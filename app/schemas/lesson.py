from typing import Optional, Literal

from pydantic import BaseModel
import enum


class LessonStatus(str, enum.Enum):
    LOCKED = "LOCKED"
    ACCESSIBLE = "ACCESSIBLE"
    ACCESSED = "ACCESSED"


class LessonNestedForm(BaseModel):
    title: str
    video_link: str


class LessonForm(LessonNestedForm):
    position: int


class LessonNestedResponse(BaseModel):
    id: int
    title: str
    position: int
    video_link: Optional[str]
    status: LessonStatus


class ModuleNestedResponse(BaseModel):
    id: int
    title: str
    position: int


class LessonResponse(LessonNestedResponse):
    parent_course_title: str
    parent_module: ModuleNestedResponse
    position_related_to_course: Literal["first", "middle", "last"]
    previous_lesson_id: Optional[int]
    next_lesson_id: Optional[int]
