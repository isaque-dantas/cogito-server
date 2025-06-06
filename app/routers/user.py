from starlette import status
from starlette.responses import Response
from fastapi import APIRouter

from app.schemas.user import UserForm, UserResponse
from app.services.auth import ActiveUser
from app.services.user import UserService

router = APIRouter(prefix="/user")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(user_form: UserForm) -> UserResponse:
    error = UserService.validate(user_form)
    if error:
        raise error

    user = UserService.register(user_form)
    user_response = UserService.to_response(user)

    return user_response


@router.get("/")
async def get(user: ActiveUser):
    if not user:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

    return UserService.to_response(user)


@router.put("/", status_code=status.HTTP_204_NO_CONTENT)
async def update(edited_data: UserForm, current_user: ActiveUser):
    error = UserService.validate(edited_data, current_user.id)
    if error:
        raise error

    UserService.update(edited_data, current_user)

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete(current_user: ActiveUser):
    UserService.delete(current_user)
