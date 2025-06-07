from typing import List

from sqlmodel import Field, SQLModel, Relationship

from app.models import Course


class Module(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    position: int

    course_id: int = Field(default=None, foreign_key="course.id")
    course: Course = Relationship(back_populates="modules")

    lessons: List["Lesson"] = Relationship(back_populates="module", cascade_delete=True)
