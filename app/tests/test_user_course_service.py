from app.services.course import CourseService
from app.services.user import UserService
from app.services.user_course import UserCourseService
from app.tests import example_test_data, reset_database


def test_has_user_already_accessed_lesson__has_not_accessed_before__should_return_false():
    reset_database()

    user = UserService.register(example_test_data['user'])
    course = CourseService.register(example_test_data['course'], user)

    assert UserCourseService.has_user_already_subscribed_to_course(course=course, user=user) == False
