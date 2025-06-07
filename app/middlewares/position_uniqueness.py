from typing import Annotated
from fastapi import HTTPException, Depends, status
from sqlmodel import select
from pydantic import BaseModel

from app.models import Session, engine, Module, Lesson
from app.middlewares.resource_existence import ExistentModule, ExistentCourse, ExistentLesson
from app.schemas.lesson import LessonForm
from app.schemas.module import ModuleForm

class ModulePositionUniquenessMiddleware:
    exception = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Position is already occupied by another instance.",
    )

    @classmethod
    def handle_existent(cls, module: ExistentModule):
        if cls.is_position_already_occupied(module.position, module.course_id, module.id):
            raise cls.exception

        return module

    @classmethod
    def handle_form(cls, module_form: ModuleForm, course: ExistentCourse):
        if cls.is_position_already_occupied(module_form.position, course.id):
            raise cls.exception

        return module_form

    @staticmethod
    def is_position_already_occupied(position: int, course_id: int, module_id: int | None = None) -> bool:
        condition = (Module.position == position) & (Module.course_id == course_id)
        if module_id is not None:
            condition = condition & (Module.id != module_id)

        with Session(engine) as session:
            modules_with_informed_position = session.scalars(
                select(Module)
                .where(condition)
            ).all()

            return len(modules_with_informed_position) > 0


class LessonPositionUniquenessMiddleware:
    exception = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Position is already occupied by another instance.",
    )

    @classmethod
    def handle_existent(cls, lesson: ExistentLesson):
        if cls.is_position_already_occupied(lesson.position, lesson.module_id, lesson.id):
            raise cls.exception

        return lesson

    @classmethod
    def handle_form(cls, lesson_form: LessonForm, module: ExistentCourse):
        if cls.is_position_already_occupied(lesson_form.position, module.id):
            raise cls.exception

        return lesson_form

    @staticmethod
    def is_position_already_occupied(position: int, module_id: int, lesson_id: int | None = None) -> bool:
        condition = (Lesson.position == position) & (Lesson.module_id == module_id)
        if lesson_id is not None:
            condition = condition & (Lesson.id != lesson_id)

        with Session(engine) as session:
            lessons_with_informed_position = session.scalars(
                select(Lesson)
                .where(condition)
            ).all()

            return len(lessons_with_informed_position) > 0


ExistentModuleWithUniquePosition = Annotated[Module, Depends(ModulePositionUniquenessMiddleware.handle_existent)]
ModuleFormWithUniquePosition = Annotated[ModuleForm, Depends(ModulePositionUniquenessMiddleware.handle_form)]

ExistentLessonWithUniquePosition = Annotated[Lesson, Depends(LessonPositionUniquenessMiddleware.handle_existent)]
LessonFormWithUniquePosition = Annotated[LessonForm, Depends(LessonPositionUniquenessMiddleware.handle_form)]

# TODO: add option for checking lesson position uniqueness
