from peewee import ForeignKeyField, CharField, IntegerField

from app.models.db import BaseModel
from app.models import Course


class Module(BaseModel):
    title = CharField()
    position = IntegerField()

    course = ForeignKeyField(Course, backref='modules', on_delete='CASCADE')
