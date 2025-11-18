# src/common/schemes.py

from pydantic import BaseModel


class CreateUserForm(BaseModel):
    username: str
    email: str
    password: str