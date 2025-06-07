from starlette import status
from fastapi import APIRouter

from app.middlewares.user_role import CoordinatorOnlyDependency
from app.middlewares.resource_existence import ExistentCourse, ExistentModule
from app.middlewares.position_uniqueness import ExistentModuleWithUniquePosition, ModuleFormWithUniquePosition

from app.schemas.module import ModuleUpdateForm
from app.services.module import ModuleService

router = APIRouter()


@router.post(
    "/course/{course_id}/module",
    status_code=status.HTTP_201_CREATED,
    dependencies=[CoordinatorOnlyDependency]
)
async def create(module_form: ModuleFormWithUniquePosition, course: ExistentCourse):
    module = ModuleService.register(module_form, course)
    return ModuleService.to_response(module)


@router.get("/module/{module_id}")
async def get(module: ExistentModule):
    return ModuleService.to_response(module)


@router.put("/module/{module_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[CoordinatorOnlyDependency])
async def update(module: ExistentModuleWithUniquePosition, edited_data: ModuleUpdateForm):
    ModuleService.update(edited_data, module)


@router.delete("/module/{module_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[CoordinatorOnlyDependency])
async def delete(module: ExistentModule):
    ModuleService.delete(module)
