from peewee import ForeignKeyField
# import enum

from app.models.db import BaseModel
from app.models import User, Lesson


# class LessonStatus(str, enum.Enum):
#     locked = "LOCKED"
#     accessible = "ACCESSIBLE"
#     accessed = "ACCESSED"


class UserAccessesLesson(BaseModel):
    user_id = ForeignKeyField(User)
    lesson_id = ForeignKeyField(Lesson)
