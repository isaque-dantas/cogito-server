from peewee import CharField, ForeignKeyField

from app.models.db import BaseModel
from app.models.user import User


class Course(BaseModel):
    title = CharField()

    user_who_created = ForeignKeyField(User, backref='courses')
