from collections.abc import Sequence
from typing import List, Optional

from app.models import Lesson, Module, User, Course, db
from app.models.user_accesses_lesson import UserAccessesLesson
from app.schemas.lesson import LessonForm, LessonResponse, LessonNestedForm, LessonStatus
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
            user_requesting_access: Optional[User] = None
    ) -> LessonResponse:
        lesson_status_for_user: LessonStatus = (
            LessonService.get_lesson_status_for_user(lesson, user_requesting_access)
        )

        should_include_video_link = (
                user_requesting_access is not None
                and
                lesson_status_for_user != LessonStatus.LOCKED
        )

        print(f"LessonService.to_response > 'id in lesson: {hasattr(lesson, 'id')}'")

        return LessonResponse(
            id=lesson.id,
            title=lesson.title,
            position=lesson.position,
            video_link=lesson.video_link if should_include_video_link else None,
            status=lesson_status_for_user
        )

    @classmethod
    def get_related_to_module(cls, module_id: int) -> Sequence[Lesson]:
        with db.atomic():
            return (
                Lesson
                .select()
                .where(Lesson.module_id == module_id)
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
                .delete()
                .where(Lesson.id == lesson.id)
            ).execute()

    @classmethod
    def register_user_access(cls, lesson: Lesson, user: User) -> None:
        if (
                cls.is_user_subscribed_in_course_of_lesson(lesson, user)
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
        if user is None:
            return LessonStatus.LOCKED

        previous_lesson: Optional[Lesson] = cls.get_previous_lesson(lesson)
        if previous_lesson is None:
            return LessonStatus.ACCESSIBLE

        if not cls.has_user_already_accessed_lesson(previous_lesson, user):
            return LessonStatus.LOCKED

        if cls.has_user_already_accessed_lesson(lesson, user):
            return LessonStatus.ACCESSED

        return LessonStatus.ACCESSIBLE

    @classmethod
    def get_previous_lesson(cls, lesson: Lesson) -> Optional[Lesson]:
        with db.atomic():
            if lesson.position == 0 and lesson.module.position == 0:
                return None

            return (
                Lesson.get_or_none(
                    (Lesson.position == lesson.position - 1)
                    &
                    (Lesson.module_id == lesson.module_id)
                )
            )

    @classmethod
    def is_user_subscribed_in_course_of_lesson(cls, lesson: Lesson, user: User):
        with db.atomic():
            related_course: Course = lesson.module.course
            return UserCourseService.has_user_already_subscribed_to_course(related_course, user)
