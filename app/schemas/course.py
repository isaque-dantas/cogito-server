from typing import Optional

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
    is_subscribed: Optional[bool]
    has_user_finished: Optional[bool]
    progress_level_percentage: Optional[float]

class CourseResponseWithCoordinatorInfo(BaseModel):
    id: int
    title: str
    not_subscribed_students: int
    subscribed_students: int
    students_who_finished: int
