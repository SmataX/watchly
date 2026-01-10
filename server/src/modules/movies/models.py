# movies/models.py

from datetime import datetime, date
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel

from typing import Optional, List
from datetime import datetime, date
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from src.modules.rating.models import RatedMovie
    from src.modules.reviews.models import Review

# --------------------
# Movie Model
# --------------------
class Movie(SQLModel, table=True):
    __tablename__ = "movies"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    overview: str
    director: str = Field(nullable=False)
    duration: int
    poster_path: Optional[str] = Field(default=None)
    release_date: Optional[date] = Field(default=None)

    # Relationships
    genres: List["MovieGenre"] = Relationship(back_populates="movie")
    ratings: List["RatedMovie"] = Relationship(back_populates="movie")
    reviews: List["Review"] = Relationship(back_populates="movie")


# --------------------
# Genre Model
# --------------------
class Genre(SQLModel, table=True):
    __tablename__ = "genre"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, nullable=False)

    # Relationships
    movies: List["MovieGenre"] = Relationship(back_populates="genre")



# --------------------
# Movie Genre (Many-to-Many Link)
# --------------------
class MovieGenre(SQLModel, table=True):
    __tablename__ = "movie_genre"

    movie_id: int = Field(foreign_key="movies.id", nullable=False, primary_key=True)
    genre_id: int = Field(foreign_key="genre.id", nullable=False, primary_key=True)

    # Relationships
    movie: Movie = Relationship(back_populates="genres")
    genre: Genre = Relationship(back_populates="movies")