from pydantic import BaseModel

from app.schemas.module import ModuleForm, ModuleResponse


class CourseForm(BaseModel):
    title: str
    modules: list[ModuleForm]


class CourseResponse(BaseModel):
    id: int
    title: str
    modules: list[ModuleResponse]
