from app.models.user import User, UserRoles
from app.models.course import Course
from app.models.module import Module
from app.models.lesson import Lesson
from app.models.user_accesses_lesson import UserAccessesLesson
from app.models.user_subscribes_in_course import UserSubscribesInCourse
from app.models.db import db

MODELS = [User, Course, Module, Lesson, UserAccessesLesson, UserSubscribesInCourse]


def create_db_and_tables():
    with db.atomic():
        db.create_tables(MODELS, safe=True)
