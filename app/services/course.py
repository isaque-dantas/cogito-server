from app.models import Course, engine, User
from app.schemas.course import CourseForm, CourseResponse
from sqlmodel import Session, insert

from app.services.module import ModuleService


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

        return CourseResponse(
            id=course.id,
            title=course.title,
            modules=[
                ModuleService.to_response(module)
                for module in modules
            ]
        )
