from datetime import datetime

from peewee import ForeignKeyField, DateTimeField

from app.models.db import BaseModel
from app.models import User, Course


class UserSubscribesInCourse(BaseModel):
    user = ForeignKeyField(User, backref='users', on_delete='CASCADE')
    course = ForeignKeyField(Course, backref='courses', on_delete='CASCADE')
    timestamp = DateTimeField(default=datetime.now)
