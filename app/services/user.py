from fastapi import HTTPException, status
import bcrypt
from pydantic import EmailStr

from app.models import User, UserRoles, db
from app.schemas.user import UserResponse, UserForm


class UserService:
    CPF_DIGITS_AMOUT = 11

    @classmethod
    def get_by_email(cls, email: str) -> User | None:
        with db.atomic():
            return User.get_or_none(User.email == email)

    @classmethod
    def get_by_id(cls, user_id: int) -> User | None:
        with db.atomic():
            return User.get(User.id == user_id)

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

        with db.atomic():
            user = User.create(
                name=user.name,
                email=user.email,
                cpf=user.cpf,
                hashed_password=user.hashed_password,
                role=user.role
            )

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
        with db.atomic():
            edited_user = cls.to_model(edited_data)

            (
                User
                .update({
                    User.name: edited_user.name,
                    User.email: edited_user.email,
                    User.cpf: edited_user.cpf,
                    User.hashed_password: edited_user.hashed_password
                })
                .where(User.id == user.id)
            ).execute()

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

    @classmethod
    def validate_unique_fields(
            cls,
            translate,
            user_form: UserForm,
            user_being_edited_id: int | None = None
    ) -> HTTPException | None:
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
            ],
            translate
        )

        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=error_detail,
        )

    @classmethod
    def get_user_with_same_unique_properties(
            cls,
            cpf: str,
            email: EmailStr,
            user_being_edited_id: int | None = None
    ) -> User | None:
        with db.atomic():
            if user_being_edited_id:
                q = (
                    User
                    .select()
                    .where(
                        (User.id != user_being_edited_id)
                        &
                        ((User.email == email) | (User.cpf == cpf))
                    )
                )
            else:
                q = (
                    User
                    .select()
                    .where(
                        ((User.email == email) | (User.cpf == cpf))
                    )
                )

            return q.execute()

    @classmethod
    def parse_error_detail_for_uniqueness_validation(cls, fields: list[str], translate) -> str:
        parsed_fields = ', '.join(
            [f"'{field}'" for field in fields]
        )

        if len(fields) > 1:
            return translate("Values for fields %s must be unique but were already registered.") % parsed_fields
        elif len(fields) == 1:
            return translate("Value for field %s must be unique but was already registered.") % parsed_fields

        return ""

    @classmethod
    def delete(cls, current_user):
        with db.atomic():
            (
                User
                .delete()
                .where(User.id == current_user.id)
            ).execute()
