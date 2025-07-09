from typing import Tuple

from peewee import fn, JOIN

from app.models import Course, User, db, UserSubscribesInCourse, Lesson, Module, UserAccessesLesson
from app.schemas.course import CourseResponseWithCoordinatorInfo


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
            ).objects()

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

    @classmethod
    def get_all_with_coordinator_info(cls):
        with db.atomic():
            raw_query = """
                        SELECT 
                            c.id,
                            c.title,
                               (SELECT COUNT(course.id)
                                FROM course
                                         JOIN usersubscribesincourse AS uc on course.id = uc.course_id
                                WHERE course.id = c.id)                                                     AS subscribed_students,

                               (
                                   (SELECT COUNT(user.id) FROM user) -
                                   (SELECT COUNT(course.id)
                                    FROM course
                                             JOIN usersubscribesincourse AS uc on course.id = uc.course_id
                                    WHERE course.id = c.id)
                                   )                                                                        AS not_subscribed_students,
                            
                               (SELECT COUNT(distinct u.id)
                                FROM user AS u
                                         JOIN usersubscribesincourse uc on u.id = uc.user_id
                                         JOIN course on uc.course_id = course.id
                                         JOIN useraccesseslesson AS ul on u.id = ul.user_id
                                WHERE course.id = c.id
                                  and (SELECT COUNT(useraccesseslesson.id)
                                       FROM useraccesseslesson
                                       WHERE useraccesseslesson.user_id = u.id) = (SELECT COUNT(lesson.id)
                                                                                   FROM lesson
                                                                                            JOIN module on lesson.module_id = module.id
                                                                                            JOIN course on module.course_id = course.id
                                                                                   WHERE course.id = c.id)) AS students_who_finished
                        FROM course c;"""

            cursor = db.execute_sql(raw_query)
            print(cursor)

            return [
                CourseResponseWithCoordinatorInfo(
                    id=row[0],
                    title=row[1],
                    subscribed_students=row[2],
                    not_subscribed_students=row[3],
                    students_who_finished=row[4],
                )
                for row in cursor.fetchall()
            ]


