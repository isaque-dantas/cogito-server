from typing import Optional

from pydantic import BaseModel

from app.schemas.lesson import LessonForm, LessonNestedForm, LessonNestedResponse


class ModuleNestedForm(BaseModel):
    title: str
    lessons: list[LessonNestedForm]


class ModuleForm(BaseModel):
    title: str
    position: int
    lessons: list[LessonForm]


class ModuleUpdateForm(BaseModel):
    title: Optional[str]
    position: Optional[int]


class ModuleResponse(BaseModel):
    id: int
    title: str
    position: int
    lessons: list[LessonNestedResponse]


