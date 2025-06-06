from typing import List

from sqlmodel import Column, Enum, Field, SQLModel, Relationship
import enum

from app.models.user_accesses_lesson import UserAccessesLessonLink


class UserRoles(str, enum.Enum):
    student = "STUDENT"
    coordinator = "COORDINATOR"

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    cpf: str = Field(unique=True)
    hashed_password: str
    role: str = Field(sa_column=Column(Enum(UserRoles), nullable=False))

    lessons: List["Lesson"] = Relationship(back_populates="users", link_model=UserAccessesLessonLink)
    courses: List["Course"] = Relationship(back_populates="user_who_created")
