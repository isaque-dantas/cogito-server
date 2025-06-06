from pydantic import BaseModel


class LessonForm(BaseModel):
    title: str
    position: int
    video_link: str


class LessonResponse(LessonForm):
    id: int
