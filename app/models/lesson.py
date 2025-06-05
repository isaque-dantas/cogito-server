from sqlmodel import Field, SQLModel, Relationship

from app.models import Module


class Lesson(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    video_link: str
    title: str
    position: int

    module_id: int = Field(default=None, foreign_key="module.id")
    module: Module = Relationship(back_populates="lessons")
