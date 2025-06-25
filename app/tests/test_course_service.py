from typing import List

from app.models import Course, Module, Lesson, User
from app.models.db import db
from app.schemas.course import CourseResponse
from app.services.course import CourseService
from app.services.user import UserService
from app.tests import example_test_data, reset_database, NUMBER_OF_LESSONS_IN_EXAMPLE_DATA


def test_create__on_happy_path__should_return_created():
    reset_database()

    user = UserService.register(example_test_data['user'])
    course = CourseService.register(example_test_data['course'], user)

    with db.atomic():
        created_course = Course.get_or_none(Course.id == course.id)
        assert created_course is not None

        created_modules: List[Module] = Module.select().where(Module.course_id == course.id).objects()
        assert len(created_modules) == len(example_test_data['course'].modules)

        created_lessons: List[Lesson] = Lesson.select().join(Module).where(Module.course_id == course.id).objects()
        assert len(created_lessons) == NUMBER_OF_LESSONS_IN_EXAMPLE_DATA

def test_to_response__on_happy_path__should_return():
    reset_database()

    user = UserService.register(example_test_data['user'])
    course = CourseService.register(example_test_data['course'], user)

    print(user, isinstance(user, User))

    with db.atomic():
        course_response = CourseService.to_response(course, user)

        assert isinstance(course_response, CourseResponse)
        assert course_response.title == course.title

        assert len(course_response.modules) == len(course.modules)
