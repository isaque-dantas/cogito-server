from pydantic import BaseModel, EmailStr, field_validator, Field
import validate_cpf

CPF_DIGITS_AMOUNT = 11


class UserResponse(BaseModel):
    name: str
    email: EmailStr
    cpf: str
    role: str


class UserForm(BaseModel):
    name: str
    email: EmailStr
    cpf: str = Field(min_length=CPF_DIGITS_AMOUNT, max_length=CPF_DIGITS_AMOUNT)
    password: str

    @field_validator('cpf', mode='after')
    @classmethod
    def is_valid_cpf(cls, cpf: str) -> str:
        if validate_cpf.is_valid(cpf):
            return cpf

        raise ValueError("The informed 'cpf' does not exist.")


class UserLoginForm(BaseModel):
    email: EmailStr
    password: str
