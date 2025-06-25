from typing import Optional

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


class LessonResponse(BaseModel):
    id: int
    title: str
    position: int
    video_link: Optional[str]
    status: Optional[LessonStatus]
