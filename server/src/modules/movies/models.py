# movies/models.py

from datetime import datetime, date
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel

from typing import Optional, List
from datetime import datetime, date
from sqlmodel import Field, SQLModel, Relationship

# --------------------
# Movie Model
# --------------------
class Movie(SQLModel, table=True):
    __tablename__ = "movies"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(nullable=False)
    overview: str
    director: str = Field(nullable=False)
    poster_path: Optional[str] = Field(default=None)
    release_date: Optional[date] = Field(default=None) # Made optional in case data is missing

    # Relationships
    genres: List["MovieGenre"] = Relationship(back_populates="movie")
    actors: List["MovieActor"] = Relationship(back_populates="movie")
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
# Actor Model
# --------------------
class Actor(SQLModel, table=True):
    __tablename__ = "actors"

    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(nullable=False)
    surname: str = Field(nullable=False)
    date_of_birth: Optional[date] = Field(default=None) # Assuming it should be a date, not a raw string
    img_path: Optional[str] = Field(default=None)

    # Relationships
    movies: List["MovieActor"] = Relationship(back_populates="actor")


# --------------------
# Movie Genre (Many-to-Many Link)
# --------------------
class MovieGenre(SQLModel, table=True):
    __tablename__ = "movie_genre"

    id: Optional[int] = Field(default=None, primary_key=True)
    movie_id: int = Field(foreign_key="movies.id", nullable=False)
    genre_id: int = Field(foreign_key="genre.id", nullable=False)

    # Relationships
    movie: Movie = Relationship(back_populates="genres")
    genre: Genre = Relationship(back_populates="movies")


# --------------------
# Movie Actor (Many-to-Many Link)
# --------------------
class MovieActor(SQLModel, table=True):
    __tablename__ = "movie_actor"

    id: Optional[int] = Field(default=None, primary_key=True)
    movie_id: int = Field(foreign_key="movies.id", nullable=False)
    actor_id: int = Field(foreign_key="actors.id", nullable=False)

    # Relationships
    movie: Movie = Relationship(back_populates="actors")
    actor: Actor = Relationship(back_populates="movies")