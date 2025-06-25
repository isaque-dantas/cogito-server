from app.models import Course, User, db, UserSubscribesInCourse


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
