from starlette import status
from starlette.responses import Response
from typing import Annotated
from fastapi import APIRouter, Depends

from app.models import User, SessionDep
from app.schemas.user import UserForm, UserResponse
from app.services.auth import AuthService
from app.services.user import UserService

router = APIRouter(prefix="/user")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(user_form: UserForm, session: SessionDep) -> UserResponse:
    user = UserService.register(user_form)
    user_response = UserService.to_response(user)

    return user_response

async def get_current_active_user(
        current_user: Annotated[User, Depends(AuthService.get_current_user)],
):
    return current_user


@router.get("/")
async def get(user: Annotated[User, Depends(get_current_active_user)]):
    if not user:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED)

    return user


@router.put("/")
async def update(user_id: int, new: User, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    user.content = new.content
    session.commit()

    return {"new_content": new.content}


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    session.delete(user)

    return None
