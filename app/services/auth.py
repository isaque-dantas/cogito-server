from typing import Annotated

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
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

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
    async def get_current_user(cls, token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = jwt.decode(token, cls.SECRET_KEY, algorithms=[cls.ALGORITHM])
            email = payload.get("sub")
            if email is None:
                raise credentials_exception

        except InvalidTokenError:
            raise credentials_exception

        user = UserService.get_by_email(email)
        if user is None:
            raise credentials_exception

        return user


async def get_current_active_user(
        current_user: Annotated[User, Depends(AuthService.get_current_user)],
):
    return current_user


ActiveUser = Annotated[User, Depends(get_current_active_user)]
