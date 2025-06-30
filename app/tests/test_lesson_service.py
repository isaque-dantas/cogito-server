from app.models import Lesson,Course
from app.models.db import db
from app.services.course import CourseService
from app.services.lesson import LessonService
from app.services.user import UserService
from app.tests import example_test_data, reset_database


def test_get_parent_titles__on_happy_path__should_return():
    reset_database()

    user = UserService.register(example_test_data['user'])
    course: Course = CourseService.register(example_test_data['course'], user)

    with db.atomic():
        parent_module = course.modules[0]
        lesson: Lesson = parent_module.lessons[0]

        parent_module_title, parent_course_title = LessonService.get_parent_titles(lesson, None, None)

        assert parent_module_title == parent_module.title
        assert parent_course_title == course.title


def test_get_position_related_to_course__on_happy_path__should_return():
    reset_database()

    user = UserService.register(example_test_data['user'])
    course: Course = CourseService.register(example_test_data['course'], user)

    with db.atomic():
        parent_module = course.modules[0]
        lesson: Lesson = parent_module.lessons[0]
        position = LessonService.get_position_related_to_course(lesson)
        assert position == 'first'

        parent_module = course.modules[-1]
        lesson: Lesson = parent_module.lessons[-1]
        position = LessonService.get_position_related_to_course(lesson)
        assert position == 'last'
