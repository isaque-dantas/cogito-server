from collections.abc import Sequence
from optparse import Option
from typing import List, Optional, Tuple, Literal

from peewee import fn

from app.models import Lesson, Module, User, Course, db, UserRoles
from app.models.user_accesses_lesson import UserAccessesLesson
from app.schemas.lesson import LessonForm, LessonResponse, LessonNestedForm, LessonStatus, LessonNestedResponse
from app.schemas.lesson import ModuleNestedResponse
from app.services.user_course import UserCourseService


class LessonService:
    @classmethod
    def create_from_form_list(cls, lessons_forms: List[LessonNestedForm], module: Module):
        with db.atomic():
            lessons = cls.get_instances_from_data(lessons_forms, module)
            Lesson.bulk_create(lessons)

    @classmethod
    def get_instances_from_data(cls, lessons_forms: List[LessonNestedForm], module: Module) -> List[Lesson]:
        return [
            Lesson(
                title=lesson_form.title,
                position=i,
                video_link=lesson_form.video_link,
                module=module
            )
            for i, lesson_form in enumerate(lessons_forms)
        ]

    @classmethod
    def to_response(
            cls,
            lesson: Lesson,
            user_requesting_access: Optional[User] = None,
            is_nested_response: bool = False
    ) -> LessonResponse | LessonNestedResponse:
        lesson_status_for_user: LessonStatus = (
            LessonService.get_lesson_status_for_user(lesson, user_requesting_access)
        )

        should_include_video_link = (
                user_requesting_access is not None
                and
                lesson_status_for_user != LessonStatus.LOCKED
        )

        if is_nested_response:
            return LessonNestedResponse(
                id=lesson.id,
                title=lesson.title,
                position=lesson.position,
                video_link=lesson.video_link if should_include_video_link else None,
                status=lesson_status_for_user,
            )

        return LessonResponse(
            id=lesson.id,
            title=lesson.title,
            position=lesson.position,
            video_link=lesson.video_link if should_include_video_link else None,
            status=lesson_status_for_user,
            # status=LessonStatus.ACCESSED,
            parent_module=ModuleNestedResponse(
                id=lesson.module.id,
                title=lesson.module.title,
                position=lesson.module.position
            ),
            parent_course_title=lesson.module.course.title,
            position_related_to_course=cls.get_position_related_to_course(lesson),
            previous_lesson_id=cls.get_previous_lesson_id(lesson),
            next_lesson_id=cls.get_next_lesson_id(lesson),
        )

    @classmethod
    def get_related_to_module(cls, module_id: int) -> Sequence[Lesson]:
        with db.atomic():
            return (
                Lesson
                .select()
                .where(Lesson.module_id == module_id)
                .order_by(Lesson.position)
            )

    @classmethod
    def register(cls, lesson_form: LessonForm, module: Module) -> Lesson:
        with db.atomic():
            return Lesson.create(
                title=lesson_form.title,
                position=lesson_form.position,
                video_link=lesson_form.video_link,
                module=module
            )

    @classmethod
    def get_by_id(cls, lesson_id: int) -> Lesson:
        with db.atomic():
            return Lesson.get_by_id(lesson_id)

    @classmethod
    def update(cls, edited_data: LessonForm, lesson: Lesson):
        with db.atomic():
            (
                Lesson
                .update({
                    Lesson.title: edited_data.title,
                    Lesson.position: edited_data.position,
                    Lesson.video_link: edited_data.video_link
                })
                .where(Lesson.id == lesson.id)
            ).execute()

    @classmethod
    def delete(cls, lesson: Lesson) -> None:
        with db.atomic():
            (
                Lesson
                .update({Lesson.position: Lesson.position - 1})
                .where((Lesson.module_id == lesson.module_id) & (Lesson.position > lesson.position))
                .execute()
            )

            (
                Lesson
                .delete()
                .where(Lesson.id == lesson.id)
                .execute()
            )

    @classmethod
    def register_user_access(cls, lesson: Lesson, user: User) -> None:
        if (
                not cls.is_user_subscribed_in_course_of_lesson(lesson, user)
                or
                cls.has_user_already_accessed_lesson(lesson, user)
        ):
            return

        with db.atomic():
            UserAccessesLesson.create(
                user_id=user.id,
                lesson_id=lesson.id
            )

    @classmethod
    def has_user_already_accessed_lesson(cls, lesson: Lesson, user: User) -> bool:
        with db.atomic():
            access = (
                UserAccessesLesson
                .select()
                .where(
                    (UserAccessesLesson.user_id == user.id)
                    &
                    (UserAccessesLesson.lesson_id == lesson.id)
                )
            )

        return bool(access)

    @classmethod
    def get_lesson_status_for_user(cls, lesson: Lesson, user: Optional[User]) -> LessonStatus:
        if (
                user is None or
                (
                        user.role != UserRoles.coordinator
                        and
                        not cls.is_user_subscribed_in_course_of_lesson(lesson, user)
                )
        ):
            return LessonStatus.LOCKED

        if cls.has_user_already_accessed_lesson(lesson, user):
            return LessonStatus.ACCESSED

        previous_lesson: Optional[Lesson] = cls.get_previous_lesson(lesson)
        if previous_lesson is None:
            return LessonStatus.ACCESSIBLE

        if user.role != UserRoles.coordinator and not cls.has_user_already_accessed_lesson(previous_lesson, user):
            return LessonStatus.LOCKED

        return LessonStatus.ACCESSIBLE

    @classmethod
    def get_previous_lesson(cls, lesson: Lesson) -> Optional[Lesson]:
        with db.atomic():
            if lesson.position == 0 and lesson.module.position == 0:
                return None

            previous_lesson_in_same_module = (
                Lesson.get_or_none(
                    (Lesson.position == lesson.position - 1)
                    &
                    (Lesson.module_id == lesson.module_id)
                )
            )

            if previous_lesson_in_same_module is not None:
                return previous_lesson_in_same_module

            max_lesson_position_for_previous_module = (
                Lesson
                .select(fn.Max(Lesson.position))
                .where(Lesson.module_id == lesson.module_id - 1)
            )

            previous_lesson_in_previous_module = (
                Lesson.get_or_none(
                    (Lesson.position.in_(max_lesson_position_for_previous_module))
                    &
                    (Lesson.module_id == lesson.module_id - 1)
                )
            )

            return previous_lesson_in_previous_module

    @classmethod
    def get_next_lesson(cls, lesson: Lesson) -> Optional[Lesson]:
        with db.atomic():
            last_lesson_of_module: Lesson = lesson.module.lessons[-1]
            last_module_of_course: Module = lesson.module.course.modules[-1]

            if lesson.position == last_lesson_of_module.position and last_module_of_course.position == 0:
                return None

            next_lesson_in_same_module = (
                Lesson.get_or_none(
                    (Lesson.position == lesson.position + 1)
                    &
                    (Lesson.module_id == lesson.module_id)
                )
            )

            if next_lesson_in_same_module is not None:
                return next_lesson_in_same_module

            first_lesson_in_next_module = (
                Lesson.get_or_none(
                    (Lesson.position == 0)
                    &
                    (Lesson.module_id == lesson.module_id + 1)
                )
            )

            return first_lesson_in_next_module

    @classmethod
    def is_user_subscribed_in_course_of_lesson(cls, lesson: Lesson, user: User):
        with db.atomic():
            related_course: Course = lesson.module.course
            return UserCourseService.has_user_already_subscribed_to_course(related_course, user)

    @classmethod
    def get_parent_titles(
            cls,
            lesson: Lesson,
            parent_module: Optional[Module],
            parent_course: Optional[Course]
    ) -> Tuple[str, str]:

        if parent_module is None or parent_course is None:
            titles = (
                Module
                .select(Module.title.alias("module_title"), Course.title.alias("course_title"))
                .join(Course)
                .where(Module.id == lesson.module_id)
            ).dicts()[0]

            parent_module_title = titles["module_title"]
            parent_course_title = titles["course_title"]
        else:
            parent_module_title = parent_module.title
            parent_course_title = parent_course.title

        return parent_module_title, parent_course_title

    @classmethod
    def get_position_related_to_course(cls, lesson) -> Literal["first", "middle", "last"]:
        if lesson.position == 0 and lesson.module.position == 0:
            return "first"

        last_lesson: Lesson = lesson.module.course.modules[-1].lessons[-1]

        if lesson.id == last_lesson.id:
            return "last"

        return "middle"

    @classmethod
    def get_previous_lesson_id(cls, lesson: Lesson) -> Optional[int]:
        previous_lesson = cls.get_previous_lesson(lesson)

        if previous_lesson is None:
            return None

        return previous_lesson.id

    @classmethod
    def get_next_lesson_id(cls, lesson) -> Optional[int]:
        next_lesson = cls.get_next_lesson(lesson)

        if next_lesson is None:
            return None

        return next_lesson.id
