# src/common/schemes.py

from pydantic import BaseModel
from datetime import datetime


class CreateUserForm(BaseModel):
    username: str
    email: str
    password: str


class AddMovieForm(BaseModel):
    title: str
    description: str
    duration: int
    poster_url: str | None = None
    release_date: datetime