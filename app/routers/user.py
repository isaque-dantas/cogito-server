from starlette import status
from fastapi import APIRouter, Request

from app.schemas.user import UserForm, UserResponse
from app.services.auth import ActiveUser
from app.services.user import UserService

router = APIRouter(prefix="/user")

@router.post("", status_code=status.HTTP_201_CREATED)
async def create(user_form: UserForm, request: Request) -> UserResponse:
    error = UserService.validate_unique_fields(request.state.translate, user_form)
    if error:
        raise error

    user = UserService.register(user_form)
    user_response = UserService.to_response(user)

    return user_response


@router.get("")
async def get(user: ActiveUser):
    return UserService.to_response(user)

@router.put("", status_code=status.HTTP_204_NO_CONTENT)
async def update(edited_data: UserForm, current_user: ActiveUser, request: Request):
    error = UserService.validate_unique_fields(request.state.translate, edited_data, current_user.id)
    if error:
        raise error

    UserService.update(edited_data, current_user)

@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete(current_user: ActiveUser):
    UserService.delete(current_user)
