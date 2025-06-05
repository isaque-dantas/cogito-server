from sqlmodel import Column, Enum, Field, SQLModel, Relationship
import enum

from app.models.user_accesses_lesson import UserAccessesLessonLink


class UserRoles(str, enum.Enum):
    student = "STUDENT"
    coordinator = "COORDINATOR"

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    email: str
    password_hash: str
    cpf: str
    role: str = Field(sa_column=Column(Enum(UserRoles), nullable=False))

    lessons: list["Lesson"] = Relationship(back_populates="users", link_model=UserAccessesLessonLink)
