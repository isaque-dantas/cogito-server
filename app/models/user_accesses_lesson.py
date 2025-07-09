from peewee import ForeignKeyField

from app.models.db import BaseModel
from app.models import User, Lesson

class UserAccessesLesson(BaseModel):
    user = ForeignKeyField(User, backref='subscribed_users', on_delete='CASCADE')
    lesson = ForeignKeyField(Lesson, backref='accessed_lessons', on_delete='CASCADE')
