from sqlmodel import Field, SQLModel, Column, Enum
# import enum


# class LessonStatus(str, enum.Enum):
#     locked = "LOCKED"
#     accessible = "ACCESSIBLE"
#     accessed = "ACCESSED"


class UserAccessesLessonLink(SQLModel, table=True):
    user_id: int | None = Field(default=None, foreign_key="user.id", primary_key=True)
    lesson_id: int | None = Field(default=None, foreign_key="lesson.id", primary_key=True)
#     status: str = Field(sa_column=Column(Enum(LessonStatus)), default=LessonStatus.locked)
