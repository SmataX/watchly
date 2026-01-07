# movies/schemes.py

from pydantic import BaseModel
from datetime import date

class AddMovieForm(BaseModel):
    title: str
    overview: str
    director: str
    duration: int
    poster_path: str | None = None
    release_date: date


class MovieData(BaseModel):
    id: int
    title: str
    poster_path: str
    release_date: date
    global_rating: int
    friends_rating: int
    user_rating: int
    genres: list[str]
    duration: int
    overview: str
