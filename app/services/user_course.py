from typing import Tuple

from peewee import fn

from app.models import Course, User, db, UserSubscribesInCourse, Lesson, Module, UserAccessesLesson


class UserCourseService:
    @classmethod
    def has_user_already_subscribed_to_course(cls, course: Course, user: User) -> bool:
        with db.atomic():
            subscription = (
                UserSubscribesInCourse
                .select()
                .where(
                    (UserSubscribesInCourse.user_id == user.id)
                    &
                    (UserSubscribesInCourse.course_id == course.id)
                )
            ).execute()

            return bool(subscription)

    @classmethod
    def subscribe(cls, course: Course, user: User) -> None:
        with db.atomic():
            UserSubscribesInCourse.create(user_id=user.id, course_id=course.id)

    @classmethod
    def get_progress_data(cls, course: Course, user: User) -> Tuple[float, bool]:
        progress_level_percentage = cls.get_progress_level_percentage_for_user(course, user)

        has_user_finished = (
            progress_level_percentage == 1.0
            if progress_level_percentage
            else None
        )

        return progress_level_percentage, has_user_finished

    @classmethod
    def get_progress_level_percentage_for_user(cls, course: Course, user: User) -> float:
        num_of_lessons: int = (
            Course
            .select(fn.count(Lesson.id).alias("num_of_lessons"))
            .join(Module)
            .join(Lesson)
            .where(Course.id == course.id)
        ).dicts()[0]["num_of_lessons"]

        num_of_seen_lessons: int = (
            UserAccessesLesson
            .select(fn.count(Lesson.id).alias("num_of_seen_lessons"))
            .join(User)
            .join(Lesson, on=(UserAccessesLesson.lesson == Lesson.id))
            .join(Module)
            .join(Course)
            .where(
                (UserAccessesLesson.user.id == user.id)
                &
                (Course.id == course.id)
            )
        ).dicts()[0]["num_of_seen_lessons"]

        return float(num_of_seen_lessons) / float(num_of_lessons)
