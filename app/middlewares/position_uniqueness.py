from typing import Annotated
from fastapi import HTTPException, Depends, status

from app.models import Module, Lesson, db
from app.middlewares.resource_existence import ExistentModule, ExistentCourse, ExistentLesson
from app.schemas.lesson import LessonForm
from app.schemas.module import ModuleForm

class ModulePositionUniquenessMiddleware:
    exception = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Position is already occupied by another instance.",
    )

    @classmethod
    def handle_existent(cls, module: ExistentModule) -> Module:
        if cls.is_position_already_occupied(module.position, module.course_id, module.id):
            raise cls.exception

        return module

    @classmethod
    def handle_form(cls, module_form: ModuleForm, course: ExistentCourse) -> ModuleForm:
        if cls.is_position_already_occupied(module_form.position, course.id):
            raise cls.exception

        return module_form

    @staticmethod
    def is_position_already_occupied(position: int, course_id: int, module_id: int | None = None) -> bool:
        condition = (Module.position == position) & (Module.course_id == course_id)
        if module_id is not None:
            condition = condition & (Module.id != module_id)

        with db.atomic():
            modules_with_informed_position = (
                Module
                .select()
                .where(condition)
            ).execute()

            return len(modules_with_informed_position) > 0


class LessonPositionUniquenessMiddleware:
    exception = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Position is already occupied by another instance.",
    )

    @classmethod
    def handle_existent(cls, lesson: ExistentLesson) -> Lesson:
        if cls.is_position_already_occupied(lesson.position, lesson.module_id, lesson.id):
            raise cls.exception

        return lesson

    @classmethod
    def handle_form(cls, lesson_form: LessonForm, module: ExistentCourse) -> LessonForm:
        if cls.is_position_already_occupied(lesson_form.position, module.id):
            raise cls.exception

        return lesson_form

    @staticmethod
    def is_position_already_occupied(position: int, module_id: int, lesson_id: int | None = None) -> bool:
        condition = (Lesson.position == position) & (Lesson.module_id == module_id)
        if lesson_id is not None:
            condition = condition & (Lesson.id != lesson_id)

        with db.atomic():
            lessons_with_informed_position = (
                Lesson
                .select()
                .where(condition)
            ).execute()

            return len(lessons_with_informed_position) > 0


ExistentModuleWithUniquePosition = Annotated[Module, Depends(ModulePositionUniquenessMiddleware.handle_existent)]
ModuleFormWithUniquePosition = Annotated[ModuleForm, Depends(ModulePositionUniquenessMiddleware.handle_form)]

ExistentLessonWithUniquePosition = Annotated[Lesson, Depends(LessonPositionUniquenessMiddleware.handle_existent)]
LessonFormWithUniquePosition = Annotated[LessonForm, Depends(LessonPositionUniquenessMiddleware.handle_form)]
