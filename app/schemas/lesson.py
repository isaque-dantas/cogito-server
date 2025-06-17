from typing import Optional

from pydantic import BaseModel
import enum


class LessonNestedForm(BaseModel):
    title: str
    video_link: str


class LessonForm(BaseModel):
    title: str
    position: int
    video_link: Optional[str]


class LessonResponse(LessonForm):
    id: int


class LessonStatus(str, enum.Enum):
    LOCKED = "LOCKED"
    ACCESSIBLE = "ACCESSIBLE"
    ACCESSED = "ACCESSED"
