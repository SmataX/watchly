from pydantic import BaseModel, field_validator, ConfigDict
from datetime import date

from .models import Genre

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

class MovieResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    poster_path: str
    release_date: date
    genres: list['GenreResponse']
    duration: int
    overview: str

    @field_validator("genres", mode="before")
    @classmethod
    def extract_genre_from_association(cls, v):
        if not v:
            return []
            
        cleaned_genres = []
        for item in v:
            if hasattr(item, "genre") and item.genre:
                cleaned_genres.append(item.genre)
            elif hasattr(item, "name"):
                cleaned_genres.append(item)
                
        return cleaned_genres

class GenreResponse(BaseModel):
    name: str
