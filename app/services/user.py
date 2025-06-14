from fastapi import HTTPException, status
from sqlmodel import Session, select, update, delete
import bcrypt
from pydantic import EmailStr
import validate_cpf

from app.models import engine
from app.models.user import User, UserRoles
from app.schemas.user import UserResponse, UserForm


class UserService:
    CPF_DIGITS_AMOUT = 11

    @classmethod
    def get_by_email(cls, email: str) -> User | None:
        with Session(engine) as session:
            return session.scalars(select(User).where(User.email == email)).first()

    @classmethod
    def get_by_id(cls, user_id: int) -> User | None:
        with Session(engine) as session:
            return session.get(User, user_id)

    @classmethod
    def to_response(cls, user: User) -> UserResponse:
        return UserResponse(
            name=user.name,
            email=user.email,
            cpf=user.cpf,
            role=user.role
        )

    @classmethod
    def register(cls, user_form: UserForm) -> User:
        user = cls.to_model(user_form)

        with Session(engine) as session:
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
            hashed_password=cls.get_password_hash(user.password),
            role=UserRoles.student
        )

    @classmethod
    def update(cls, edited_data: UserForm, user: User) -> None:
        with Session(engine) as session:
            edited_user = cls.to_model(edited_data)
            print(edited_user.name)

            session.exec(
                update(User)
                .where(User.id == user.id)
                .values(
                    name=edited_user.name,
                    email=edited_user.email,
                    cpf=edited_user.cpf,
                    hashed_password=edited_user.hashed_password
                )
            )

            session.commit()

    @classmethod
    def get_password_hash(cls, password) -> str:
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
        return hashed_password.decode('utf-8')

    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        plain_encoded = plain_password.encode('utf-8')
        hashed_encoded = hashed_password.encode('utf-8')

        return bcrypt.checkpw(password=plain_encoded, hashed_password=hashed_encoded)

    # @classmethod
    # def get_exception_for_cpf_and_email(cls, cpf: str, email: EmailStr) -> HTTPException | None:
    #     invalid_fields: list[str] = []
    #     detail: dict[str, str] = {}
    #
    #     cpf_error_detail = cls.get_cpf_error_detail(cpf)
    #     if cpf_error_detail:
    #         detail.update({"cpf": cpf_error_detail})
    #
    #     email_error_detail = cls.get_email_error_detail(email)
    #     if email_error_detail:
    #         detail.update({"email": email_error_detail})
    #
    #     if not invalid_fields:
    #         return None
    #
    #     return HTTPException(
    #         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    #         detail=detail
    #     )
    #
    # @classmethod
    # def get_cpf_error_detail(cls, cpf: str) -> str | None:
    #     is_valid = validate_cpf.is_valid(cpf)
    #
    #     if is_valid:
    #         return None
    #
    #     if len(cpf) != cls.CPF_DIGITS_AMOUT:
    #         return f"The 'cpf' must have {cls.CPF_DIGITS_AMOUT} characters, but has {len(cpf)}"
    #
    #     return "The informed 'cpf' does not exist."

    @classmethod
    def validate_unique_fields(cls, user_form: UserForm,
                               user_being_edited_id: int | None = None) -> HTTPException | None:
        previously_registered_user_with_same_properties: User = (
            cls.get_user_with_same_unique_properties(
                cpf=user_form.cpf,
                email=user_form.email,
                user_being_edited_id=user_being_edited_id
            )
        )

        if not previously_registered_user_with_same_properties:
            return None

        unique_fields: list[str] = ['cpf', 'email']
        error_detail = cls.parse_error_detail_for_uniqueness_validation(
            [
                field for field in unique_fields
                if getattr(previously_registered_user_with_same_properties, field) == getattr(user_form, field)
            ]
        )

        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_detail,
        )

    @classmethod
    def get_user_with_same_unique_properties(
            cls,
            cpf: str,
            email: EmailStr,
            user_being_edited_id: int | None = None
    ) -> User | None:
        with Session(engine) as session:
            if user_being_edited_id:
                stmt = (
                    select(User)
                    .where(User.id != user_being_edited_id)
                    .where((User.email == email) | (User.cpf == cpf))
                )
            else:
                stmt = (
                    select(User)
                    .where((User.email == email) | (User.cpf == cpf))
                )

            return session.scalars(stmt).first()

    @classmethod
    def parse_error_detail_for_uniqueness_validation(cls, fields: list[str]) -> str:
        parsed_fields = ', '.join(
            [f"'{field}'" for field in fields]
        )

        if len(fields) > 1:
            return f"Values for fields {parsed_fields} must be unique but were already registered."
        elif len(fields) == 1:
            return f"Value for field {parsed_fields} must be unique but was already registered."

        return ""

    @classmethod
    def delete(cls, current_user):
        with Session(engine) as session:
            session.exec(
                delete(User)
                .where(User.id == current_user.id)
            )

            session.commit()
