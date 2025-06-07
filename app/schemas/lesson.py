from pydantic import BaseModel


class LessonNestedForm(BaseModel):
    title: str
    video_link: str


class LessonForm(BaseModel):
    title: str
    position: int
    video_link: str


class LessonResponse(LessonForm):
    id: int
