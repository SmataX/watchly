from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import BaseModel

from src.modules.movies.models import Movie
from src.modules.auth.models import User


class RatingCreateForm(BaseModel):
    movie_id: int
    rating: int

class RatingGetForm(BaseModel):
    id: int

class RatingUpdateForm(BaseModel):
    id: int
    rating: int

class RatingResponse(BaseModel):
    movie: Movie
    user: User
    rating: int
    created_at: datetime