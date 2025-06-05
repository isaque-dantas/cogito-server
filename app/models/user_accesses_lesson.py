from sqlmodel import Field, SQLModel


class UserAccessesLessonLink(SQLModel, table=True):
    user_id: int | None = Field(default=None, foreign_key="user.id", primary_key=True)
    lesson_id: int | None = Field(default=None, foreign_key="lesson.id", primary_key=True)
