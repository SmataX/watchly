# movies/models.py

from datetime import datetime, date
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from sqlalchemy import Column, JSON

if TYPE_CHECKING:
    from src.modules.rating.models import RatedMovie
    from src.modules.reviews.models import Review


# --------------------
# Movie Genre (Many-to-Many Link)
# --------------------
class MovieGenre(SQLModel, table=True):
    __tablename__ = "movie_genre"

    movie_id: int = Field(foreign_key="movies.id", nullable=False, primary_key=True)
    genre_id: int = Field(foreign_key="genre.id", nullable=False, primary_key=True)

    # Relationships
    # movie: 'Movie' = Relationship(back_populates="genres")
    # genre: Genre = Relationship(back_populates="movies")


class Genre(SQLModel, table=True):
    __tablename__ = "genre"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, nullable=False)

    # Relationships
    movies: List["Movie"] = Relationship(back_populates="genres", link_model=MovieGenre)


class Movie(SQLModel, table=True):
    __tablename__ = "movies"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    overview: str
    director: str = Field(nullable=False)
    actors: str = Field(nullable=True)
    duration: int
    poster_path: Optional[str] = Field(default=None)
    release_date: Optional[date] = Field(default=None)
    trailer_url: Optional[str] = Field(default=None)
    backdrop_url: Optional[str] = Field(default=None)
    photos: List[str] = Field(default=[], sa_column=Column(JSON))

    # Relationships
    genres: List["Genre"] = Relationship(back_populates="movies", link_model=MovieGenre)
    ratings: List["RatedMovie"] = Relationship(back_populates="movie")
    reviews: List["Review"] = Relationship(back_populates="movie")