from pydantic import BaseModel

from app.schemas.module import ModuleResponse, ModuleNestedForm
from app.schemas.user import UserResponse


class CourseForm(BaseModel):
    title: str
    modules: list[ModuleNestedForm]

class CoursePatchForm(BaseModel):
    title: str


class CourseResponse(BaseModel):
    id: int
    title: str
    modules: list[ModuleResponse]
    user_who_created: UserResponse
