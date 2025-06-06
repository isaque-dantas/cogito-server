from pydantic import BaseModel

class UserResponse(BaseModel):
    name: str
    email: str
    cpf: str
    role: str

class UserForm(BaseModel):
    name: str
    email: str
    cpf: str
    password: str

class UserLoginForm(BaseModel):
    email: str
    password: str
