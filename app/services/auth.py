from typing import Annotated, Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel

from datetime import datetime, timedelta, timezone
from app.services.user import UserService
from app.models.user import User


class Token(BaseModel):
    access_token: str
    token_type: str


class AuthService:
    unauthorized_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    mandatory_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=True)
    possible_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 120

    @classmethod
    def authenticate_user(cls, email: str, password: str):
        user: User | None = UserService.get_by_email(email)
        if not user:
            return False
        if not UserService.verify_password(password, user.hashed_password):
            return False
        return user

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=cls.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, cls.SECRET_KEY, algorithm=cls.ALGORITHM)

        return encoded_jwt

    @classmethod
    async def get_user_from_token(cls, token: str):
        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            email = payload.get("sub")
            if email is None:
                raise cls.unauthorized_error

        except InvalidTokenError:
            raise cls.unauthorized_error

        user = UserService.get_by_email(email)
        if user is None:
            raise cls.unauthorized_error

        return user

    @classmethod
    async def get_mandatory_current_user(cls, token: Annotated[str, Depends(mandatory_oauth2_scheme)]):
        return cls.get_user_from_token(token)

    @classmethod
    async def get_possible_current_user(cls, token: Annotated[Optional[str], Depends(possible_oauth2_scheme)]) -> Optional[User]:
        if token is None:
            return None

        return await cls.get_user_from_token(token)


async def get_current_active_user(
        current_user: Annotated[User, Depends(AuthService.get_mandatory_current_user)],
):
    return current_user


async def get_possible_current_active_user(
        current_user: Annotated[Optional[User], Depends(AuthService.get_possible_current_user)],
):
    return current_user


ActiveUser = Annotated[User, Depends(get_current_active_user)]
PossibleActiveUser = Annotated[User, Depends(get_possible_current_active_user)]
