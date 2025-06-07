from starlette import status
from fastapi import APIRouter

from app.middlewares.user_role import CoordinatorOnlyDependency, CoordinatorLogged
from app.middlewares.resource_existence import ExistentCourse
from app.schemas.course import CourseForm, CoursePatchForm
from app.services.course import CourseService

router = APIRouter(prefix="/course")


@router.post("", status_code=status.HTTP_201_CREATED)
async def create(course_form: CourseForm, current_user: CoordinatorLogged):
    course = CourseService.register(course_form, current_user)
    return CourseService.to_response(course)


@router.get("")
async def get_all():
    return CourseService.get_all()


@router.get("/{course_id}")
async def get(course: ExistentCourse):
    return CourseService.to_response(course)


@router.patch("/{course_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[CoordinatorOnlyDependency])
async def patch(course: ExistentCourse, edited_data: CoursePatchForm):
    CourseService.patch(edited_data, course)


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[CoordinatorOnlyDependency])
async def delete(course: ExistentCourse):
    CourseService.delete(course)
