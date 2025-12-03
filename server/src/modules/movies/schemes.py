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