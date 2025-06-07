from typing import List, Sequence

from sqlmodel import Session, select, update, delete

from app.models import Module, Course, engine
from app.schemas.module import ModuleForm, ModuleResponse, ModuleUpdateForm, ModuleNestedForm
from app.services.lesson import LessonService


class ModuleService:
    @classmethod
    def get_instances_from_data(cls, modules_forms: List[ModuleNestedForm]) -> List[Module]:
        return [
            Module(
                title=module_form.title,
                position=i,
                lessons=LessonService.get_instances_from_data(module_form.lessons),
            )
            for i, module_form in enumerate(modules_forms)
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

    @classmethod
    def register(cls, module_form: ModuleForm, course: Course) -> Module:
        with Session(engine) as session:
            module = Module(
                title=module_form.title,
                position=module_form.position,
                lessons=module_form.lessons,
                course=course,
            )

            session.add(module)
            session.commit()
            session.refresh(module)

            return module

    @classmethod
    def get_by_id(cls, module_id: int):
        with Session(engine) as session:
            return session.get(Module, module_id)

    @classmethod
    def update(cls, edited_data: ModuleUpdateForm, module: Module):
        with Session(engine) as session:
            session.exec(
                update(Module)
                .where(Module.id == module.id)
                .values(
                    title=edited_data.title,
                    position=edited_data.position
                )
            )

            session.commit()

    @classmethod
    def delete(cls, module: Module):
        with Session(engine) as session:
            session.delete(module)
            session.commit()
