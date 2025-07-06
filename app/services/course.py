from typing import Optional, List

from app.models import Course, User, db
from app.schemas.course import CourseForm, CourseResponse, CoursePatchForm

from app.services.module import ModuleService
from app.services.user import UserService
from app.services.user_course import UserCourseService


class CourseService:
    @classmethod
    def register(cls, course_form: CourseForm, user_who_created: User) -> Course:
        with db.atomic():
            course = Course.create(
                title=course_form.title,
                user_who_created=user_who_created
            )

            ModuleService.create_from_form_list(course_form.modules, course)

            return course

    @classmethod
    def to_response(cls, course: Course, user_requesting_access: Optional[User]) -> CourseResponse:
        modules = ModuleService.get_related_to_course(course.id)
        user_who_created: User = UserService.get_by_id(course.user_who_created_id)

        is_subscribed = (
            UserCourseService.has_user_already_subscribed_to_course(course, user_requesting_access)
            if user_requesting_access
            else False
        )

        if is_subscribed:
            progress_level_percentage, has_user_finished = (
                UserCourseService.get_progress_data(course, user_requesting_access)
            )
        else:
            progress_level_percentage, has_user_finished = (None, None)

        return CourseResponse(
            id=course.id,
            title=course.title,
            modules=[
                ModuleService.to_response(module, user_requesting_access)
                for module in modules
            ],
            user_who_created=UserService.to_response(user_who_created),
            is_subscribed=is_subscribed,
            progress_level_percentage=progress_level_percentage,
            has_user_finished=has_user_finished,
        )

    @classmethod
    def get_all(cls, user_requesting_access: Optional[User]):
        with db.atomic():
            courses: List[Course] = Course.select().objects()
            return [
                CourseService.to_response(course, user_requesting_access)
                for course in courses
            ]

    @classmethod
    def get_by_id(cls, course_id: int) -> Course | None:
        with db.atomic():
            return Course.get(Course.id == course_id)

    @classmethod
    def patch(cls, edited_data: CoursePatchForm, course: Course):
        with db.atomic():
            (
                Course
                .update({Course.title: edited_data.title})
                .where(Course.id == course.id)
            ).execute()

    @classmethod
    def delete(cls, course: Course):
        with db.atomic():
            (
                Course
                .delete()
                .where(Course.id == course.id)
            ).execute()

    @classmethod
    def get_all_matching_title(cls, user: Optional[User], q: str) -> List[CourseResponse]:
        with db.atomic():
            courses: List[Course] = Course.select().where(Course.title.contains(q)).objects()
            return [
                cls.to_response(course, user)
                for course in courses
            ]
