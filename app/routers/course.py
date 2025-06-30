from starlette import status
from fastapi import APIRouter, Response, Request, HTTPException

from app.middlewares.user_role import CoordinatorOnlyDependency, CoordinatorLogged
from app.middlewares.resource_existence import ExistentCourse
from app.schemas.course import CourseForm, CoursePatchForm
from app.services.auth import ActiveUser, PossibleActiveUser
from app.services.course import CourseService
from app.services.user_course import UserCourseService

router = APIRouter(prefix="/course")


@router.post("", status_code=status.HTTP_201_CREATED)
async def create(course_form: CourseForm, current_user: CoordinatorLogged):
    course = CourseService.register(course_form, current_user)
    return CourseService.to_response(course, current_user)


@router.get("")
async def get_all(current_user: PossibleActiveUser):
    return CourseService.get_all(current_user)


@router.get("/{course_id}")
async def get(course: ExistentCourse, current_user: PossibleActiveUser):
    return CourseService.to_response(course, current_user)


@router.patch("/{course_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[CoordinatorOnlyDependency])
async def patch(course: ExistentCourse, edited_data: CoursePatchForm):
    CourseService.patch(edited_data, course)


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[CoordinatorOnlyDependency])
async def delete(course: ExistentCourse):
    CourseService.delete(course)


@router.post("/{course_id}/subscribe", status_code=status.HTTP_200_OK)
async def subscribe(course: ExistentCourse, current_user: ActiveUser, request: Request):
    if UserCourseService.has_user_already_subscribed_to_course(course, current_user):
        raise HTTPException(
            detail=request.state.translate("You have already subscribed to this course."),
            status_code=status.HTTP_409_CONFLICT
        )

    UserCourseService.subscribe(course, current_user)

    return CourseService.to_response(course, current_user)
