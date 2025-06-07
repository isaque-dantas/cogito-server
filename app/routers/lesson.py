from starlette import status
from fastapi import APIRouter

from app.middlewares.user_role import CoordinatorOnlyDependency
from app.middlewares.resource_existence import ExistentLesson, ExistentModule
from app.middlewares.position_uniqueness import ExistentLessonWithUniquePosition, LessonFormWithUniquePosition
from app.schemas.lesson import LessonForm
from app.services.auth import PossibleActiveUser
from app.services.lesson import LessonService

router = APIRouter()


@router.post(
    "/module/{module_id}/lesson",
    status_code=status.HTTP_201_CREATED,
    dependencies=[CoordinatorOnlyDependency]
)
async def create(lesson_form: LessonFormWithUniquePosition, module: ExistentModule):
    lesson = LessonService.register(lesson_form, module)
    return LessonService.to_response(lesson)


@router.get("/lesson/{lesson_id}")
async def get(lesson: ExistentLesson, possible_current_user: PossibleActiveUser):
    if possible_current_user:
        LessonService.register_user_access(lesson, possible_current_user)

    return LessonService.to_response(lesson)


@router.put("/lesson/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[CoordinatorOnlyDependency])
async def update(lesson: ExistentLessonWithUniquePosition, edited_data: LessonForm):
    LessonService.update(edited_data, lesson)


@router.delete("/lesson/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[CoordinatorOnlyDependency])
async def delete(lesson: ExistentLesson):
    LessonService.delete(lesson)
