from fastapi import HTTPException, status, APIRouter

from app.schemas.user import UserLoginForm
from app.services.auth import Token, AuthService

router = APIRouter(prefix="/auth")


@router.post("/token")
async def login_for_access_token(form_data: UserLoginForm) -> Token:
    user = AuthService.authenticate_user(form_data.email, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = AuthService.create_access_token(data={"sub": user.email})

    return Token(access=access_token, type="bearer")
