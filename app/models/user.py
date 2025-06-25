from peewee import CharField
import enum

from app.models.db import BaseModel


class UserRoles(str, enum.Enum):
    student = "STUDENT"
    coordinator = "COORDINATOR"


class User(BaseModel):
    name = CharField()
    email = CharField(unique=True)
    cpf = CharField(unique=True)
    hashed_password = CharField()
    role = CharField(max_length=11, choices=[
        ("student", UserRoles.student),
        ("coordinator", UserRoles.coordinator),
    ])
