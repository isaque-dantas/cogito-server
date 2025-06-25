from datetime import datetime

from peewee import ForeignKeyField, DateTimeField

from app.models.db import BaseModel
from app.models import User

class UserSubscribesInCourse(BaseModel):
    user_id = ForeignKeyField(User, backref='users', on_delete='CASCADE')
    course_id = ForeignKeyField(User, backref='courses', on_delete='CASCADE')
    timestamp = DateTimeField(default=datetime.now)
