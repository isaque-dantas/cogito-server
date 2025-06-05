from typing import List

from sqlmodel import Field, SQLModel, Relationship

from app.models import Course


class Module(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    position: int
    title: str

    course_id: int = Field(default=None, foreign_key="course.id")
    course: Course = Relationship(back_populates="modules")

    lessons: List["Course"] = Relationship(back_populates="module")
