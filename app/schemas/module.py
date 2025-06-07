from pydantic import BaseModel

from app.schemas.lesson import LessonForm, LessonResponse, LessonNestedForm


class ModuleNestedForm(BaseModel):
    title: str
    lessons: list[LessonNestedForm]

class ModuleForm(BaseModel):
    title: str
    position: int
    lessons: list[LessonForm]


class ModuleUpdateForm(BaseModel):
    title: str
    position: int

class ModuleResponse(BaseModel):
    id: int
    title: str
    position: int
    lessons: list[LessonResponse]
