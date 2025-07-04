from typing import List, Sequence, Optional

from app.models import Module, Course, User, db
from app.schemas.lesson import LessonResponse, LessonStatus
from app.schemas.module import ModuleForm, ModuleResponse, ModuleUpdateForm, ModuleNestedForm
from app.services.lesson import LessonService


class ModuleService:
    @classmethod
    def create_from_form_list(cls, modules_forms: List[ModuleNestedForm], course: Course) -> None:
        with db.atomic():
            for i, module_form in enumerate(modules_forms):
                module = Module.create(title=module_form.title, position=i, course=course)
                LessonService.create_from_form_list(module_form.lessons, module)

    @classmethod
    def to_response(cls, module: Module, user_requesting_access: Optional[User]) -> ModuleResponse:
        # lessons = LessonService.get_related_to_module(module.id)

        return ModuleResponse(
            id=module.id,
            title=module.title,
            position=module.position,
            lessons=[
                LessonService.to_response(lesson, user_requesting_access, is_nested_response=True)
                for lesson in module.lessons
            ],
        )

    @classmethod
    def get_related_to_course(cls, course_id: int) -> Sequence[Module]:
        with db.atomic():
            return (
                Module
                .select()
                .where(Module.course_id == course_id)
            )

    @classmethod
    def register(cls, module_form: ModuleForm, course: Course) -> Module:
        with db.atomic():
            module: Module = Module.create(
                title=module_form.title,
                position=module_form.position,
                course=course,
            )

            LessonService.create_from_form_list(module_form.lessons, module)

            return module

    @classmethod
    def get_by_id(cls, module_id: int):
        with db.atomic():
            return Module.get_by_id(module_id)

    @classmethod
    def update(cls, edited_data: ModuleUpdateForm, module: Module):
        data_to_update = {}
        if edited_data.title is not None:
            data_to_update.update({Module.title: edited_data.title})
        if edited_data.position is not None:
            data_to_update.update({Module.position: edited_data.position})

        if not edited_data:
            return

        with db.atomic():
            (
                Module
                .update(data_to_update)
                .where(Module.id == module.id)
            ).execute()

    @classmethod
    def delete(cls, module: Module):
        with db.atomic():
            (
                Module
                .update({Module.position: Module.position - 1})
                .where((Module.course.id == module.course.id) & (Module.position > module.position))
                .execute()
            )

            (
                Module
                .delete()
                .where(Module.id == module.id)
            ).execute()
