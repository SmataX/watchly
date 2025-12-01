# movies/schemes.py

from pydantic import BaseModel
from datetime import date

class AddMovieForm(BaseModel):
    title: str
    description: str
    duration: int
    poster_url: str | None = None
    release_date: date