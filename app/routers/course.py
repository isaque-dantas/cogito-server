from starlette import status
from starlette.responses import Response
from fastapi import APIRouter

from app.schemas.course import CourseForm, CourseResponse
from app.services.auth import ActiveUser
from app.services.course import CourseService

router = APIRouter(prefix="/course")


@router.post("", status_code=status.HTTP_201_CREATED)
async def create(course_form: CourseForm, current_user: ActiveUser) -> CourseResponse:
    course = CourseService.register(course_form, current_user)
    course_response = CourseService.to_response(course)

    return course_response


@router.get("/")
async def get():
    return "foo"


@router.get("/<course_id>")
async def get(course_id: int):
    if not CourseService.exists(course_id):
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

    return "foo"


@router.put("/<course_id>", status_code=status.HTTP_204_NO_CONTENT)
async def update(edited_data: CourseForm, current_user: ActiveUser):
    error = CourseService.validate(edited_data, current_user.id)
    if error:
        raise error

    CourseService.update(edited_data, current_user)


@router.delete("/<course_id>", status_code=status.HTTP_204_NO_CONTENT)
async def delete(current_user: ActiveUser):
    CourseService.delete(current_user)
