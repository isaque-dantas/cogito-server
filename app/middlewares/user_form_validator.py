from http.client import HTTPException

from app.schemas.user import UserForm
from app.services.user import UserService

class UserFormValidatorMiddleware:
    def __call__(self, user_form: UserForm) -> UserForm:
        ...
