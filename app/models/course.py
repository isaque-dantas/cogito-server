from typing import List

from sqlmodel import Field, SQLModel, Relationship
from app.models.user import User

class Course(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str

    user_who_created_id: int = Field(default=None, foreign_key="user.id")
    user_who_created: User = Relationship(back_populates="courses")

    modules: List["Module"] = Relationship(back_populates="courses")
