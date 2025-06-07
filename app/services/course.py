from typing import Sequence

from app.models import Course, engine, User
from app.schemas.course import CourseForm, CourseResponse, CoursePatchForm
from sqlmodel import Session, select, update, delete

from app.services.module import ModuleService
from app.services.user import UserService


class CourseService:
    @classmethod
    def register(cls, course_form: CourseForm, user_who_created: User) -> Course:
        with Session(engine) as session:
            course = Course(
                title=course_form.title,
                modules=ModuleService.get_instances_from_data(course_form.modules),
                user_who_created=user_who_created
            )

            session.add(course)
            session.commit()
            session.refresh(course)

            return course

    @classmethod
    def to_response(cls, course: Course) -> CourseResponse:
        modules = ModuleService.get_related_to_course(course.id)
        user: User = UserService.get_by_id(course.user_who_created_id)

        return CourseResponse(
            id=course.id,
            title=course.title,
            modules=[
                ModuleService.to_response(module)
                for module in modules
            ],
            user_who_created=UserService.to_response(user)
        )

    @classmethod
    def get_all(cls):
        with Session(engine) as session:
            courses: Sequence[Course] = session.scalars(select(Course)).all()
            return [
                CourseService.to_response(course)
                for course in courses
            ]

    @classmethod
    def get_by_id(cls, course_id: int) -> Course | None:
        with Session(engine) as session:
            return session.get(Course, course_id)

    @classmethod
    def patch(cls, edited_data: CoursePatchForm, course: Course):
        with Session(engine) as session:
            session.exec(
                update(Course)
                .where(Course.id == course.id)
                .values(title=edited_data.title)
            )

            session.commit()

    @classmethod
    def delete(cls, course: Course):
        with Session(engine) as session:
            session.delete(course)
            session.commit()
