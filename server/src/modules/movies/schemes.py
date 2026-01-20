from pydantic import BaseModel, field_validator, ConfigDict
from datetime import date
from typing import Optional, List

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
    trailer_url: Optional[str] = None
    backdrop_url: Optional[str] = None
    photos: List[str] = []

    @field_validator('photos', mode='before')
    @classmethod
    def check_photos(cls, v):
        if v is None:
            return []
        return v

class GenreResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    name: str
