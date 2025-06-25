from typing import List

from app.models import Course, Module, Lesson, User
from app.models.db import db
from app.schemas.course import CourseResponse
from app.schemas.module import ModuleResponse
from app.services.course import CourseService
from app.services.module import ModuleService
from app.services.user import UserService
from app.tests import example_test_data, reset_database, NUMBER_OF_LESSONS_IN_EXAMPLE_DATA


def test_to_response__on_happy_path__should_return():
    reset_database()

    user = UserService.register(example_test_data['user'])
    course = CourseService.register(example_test_data['course'], user)
    module = course.modules[0]

    module_response = ModuleService.to_response(module, user)
    print(module_response.lessons)

    assert isinstance(module_response, ModuleResponse)
    assert module_response.title == module.title

    assert len(module_response.lessons) == len(module_response.lessons)

