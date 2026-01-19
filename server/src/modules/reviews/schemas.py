from pydantic import BaseModel, field_validator
from datetime import datetime, date
from typing import Optional

from src.modules.auth.models import User
from src.modules.movies.schemes import MovieResponse

class ReviewCreateForm(BaseModel):
    movie_id: int
    content: str

class ReviewGetForm(BaseModel):
    id: int


class ReviewResponse(BaseModel):
    id: int
    content: str
    created_at: date
    user: User
    movie: Optional[MovieResponse]

    @field_validator('created_at', mode='before')
    @classmethod
    def strip_time(cls, v):
        if isinstance(v, datetime):
            return v.date()
        return v