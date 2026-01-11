from pydantic import BaseModel
from datetime import datetime
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
    created_at: datetime
    user: User
    movie: Optional[MovieResponse]