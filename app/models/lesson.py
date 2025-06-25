from peewee import CharField, IntegerField, ForeignKeyField

from app.models.db import BaseModel
from app.models import Module


class Lesson(BaseModel):
    title = CharField()
    position = IntegerField()
    video_link = CharField(max_length=64)

    module = ForeignKeyField(Module, backref='lessons', on_delete='CASCADE')
