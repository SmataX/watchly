from pydantic import BaseModel, field_validator, ConfigDict
from datetime import date
from typing import Optional

from .models import Genre

class AddMovieForm(BaseModel):
    title: str
    overview: str
    director: str
    duration: int
    poster_path: str | None = None
    release_date: date


class MovieData(BaseModel):
    movie: 'MovieResponse' 
    avg_rating: float
    user_rating: Optional[float] = 0.0
    friends_rating: Optional[float] = 0.0
    
    model_config = ConfigDict(from_attributes=True)

class MovieResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    poster_path: Optional[str]
    release_date: date
    genres: list['GenreResponse']
    director: str
    actors: Optional[str]
    duration: Optional[int]
    overview: Optional[str]

class GenreResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
