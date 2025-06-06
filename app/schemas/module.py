from typing import List

from pydantic import BaseModel

from app.schemas.lesson import LessonForm, LessonResponse


class ModuleForm(BaseModel):
    title: str
    position: int
    lessons: list[LessonForm]


class ModuleResponse(BaseModel):
    id: int
    title: str
    position: int
    lessons: list[LessonResponse]
