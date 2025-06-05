from passlib.context import CryptContext

from app.models import get_session
from sqlmodel import select

from app.models.user import User, UserRoles
from app.schemas.user import UserResponse, UserForm


class UserService:
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def get_by_username(cls, username) -> User | None:
        session = get_session()
        return session.execute(select(User).where(User.username == username))

    @classmethod
    def to_response(cls, user: UserForm) -> UserResponse:
        return UserResponse(
            name=user.name,
            email=user.email,
            username=user.username,
            cpf=user.cpf
        )

    @classmethod
    def register(cls, user_form: UserForm) -> User:
        session = get_session()

        user = cls.to_model(user_form)

        session.add(user)
        session.commit()
        session.refresh(user)

        return user

    @classmethod
    def to_model(cls, user: UserForm) -> User:
        return User(
            name=user.name,
            cpf=user.cpf,
            email=user.email,
            username=user.username,
            hashed_password=cls.get_password_hash(user.password),
            role=UserRoles.student
        )

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return cls.password_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, password):
        return cls.password_context.hash(password)
