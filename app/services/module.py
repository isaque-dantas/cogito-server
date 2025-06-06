from typing import List, Sequence

from sqlmodel import Session, select

from app.models import Module, Course, engine, Lesson
from app.schemas.module import ModuleForm, ModuleResponse
from app.services.lesson import LessonService


class ModuleService:
    @classmethod
    def get_instances_from_data(cls, modules_forms: List[ModuleForm]) -> List[Module]:
        return [
            Module(
                title=module_form.title,
                position=module_form.position,
                lessons=LessonService.get_instances_from_data(module_form.lessons),
            )
            for module_form in modules_forms
        ]

    @classmethod
    def to_response(cls, module) -> ModuleResponse:
        lessons = LessonService.get_related_to_module(module.id)

        return ModuleResponse(
            id=module.id,
            title=module.title,
            position=module.position,
            lessons=[
                LessonService.to_response(lesson)
                for lesson in lessons
            ],
        )

    @classmethod
    def get_related_to_course(cls, course_id: int) -> Sequence[Module]:
        with Session(engine) as session:
            return session.scalars(
                select(Module).where(Module.course_id == course_id)
            ).all()
