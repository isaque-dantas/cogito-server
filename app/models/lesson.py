from sqlmodel import Field, SQLModel, Relationship

from app.models import Module, User
from app.models.user_accesses_lesson import UserAccessesLessonLink


class Lesson(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    video_link: str
    title: str
    position: int

    module_id: int = Field(default=None, foreign_key="module.id")
    module: Module = Relationship(back_populates="lessons")

    users: list["User"] = Relationship(back_populates="lessons", link_model=UserAccessesLessonLink)
