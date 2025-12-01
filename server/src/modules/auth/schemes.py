from pydantic import BaseModel
from datetime import datetime, date

class RegisterUserScheme(BaseModel):
    username: str
    email: str
    password: str

class LoginUserScheme(BaseModel):
    username: str
    password: str