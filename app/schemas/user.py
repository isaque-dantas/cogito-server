from pydantic import BaseModel

class UserResponse(BaseModel):
    name: str
    email: str
    username: str
    cpf: str

class UserForm(UserResponse):
    password: str
