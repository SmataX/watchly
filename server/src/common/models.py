from datetime import datetime, date
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel

from typing import Optional, List
from datetime import datetime, date
from sqlmodel import Field, SQLModel, Relationship

# --- Core Tables ---

# --------------------
# User Model
# --------------------
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    password: str = Field(nullable=False)
    profile_url: Optional[str] = Field(default=None) # Renamed to match DBML
    description: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationships (Optional: for ease of use in SQLModel)
    rated_movies: List["RatedMovie"] = Relationship(back_populates="user")
    reviews: List["Review"] = Relationship(back_populates="user")
    # Note: Friends relationship is complex in SQLModel/SQLAlchemy and often handled separately or via explicit association objects.

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
# Genre Model
# --------------------
class Genre(SQLModel, table=True):
    __tablename__ = "genre"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, nullable=False)

    # Relationships
    movies: List["MovieGenre"] = Relationship(back_populates="genre")

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

# --- Association/Linking Tables ---

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

# --------------------
# Rated Movies (User Ratings)
# --------------------
class RatedMovie(SQLModel, table=True):
    __tablename__ = "ratedmovies"

    id: Optional[int] = Field(default=None, primary_key=True)
    movie_id: int = Field(foreign_key="movies.id", nullable=False)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    value: int = Field(nullable=False) # Rating value

    # Relationships
    movie: Movie = Relationship(back_populates="ratings")
    user: User = Relationship(back_populates="rated_movies")

# --------------------
# Reviews
# --------------------
class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    id: Optional[int] = Field(default=None, primary_key=True)
    movie_id: int = Field(foreign_key="movies.id", nullable=False)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    value: str = Field(nullable=False) # Review content

    # Relationships
    movie: Movie = Relationship(back_populates="reviews")
    user: User = Relationship(back_populates="reviews")

# --------------------
# Friends
# --------------------
class Friend(SQLModel, table=True):
    __tablename__ = "friends"

    id: Optional[int] = Field(default=None, primary_key=True)
    # user_1 and user_2 are both foreign keys to the Users table
    user_1: int = Field(foreign_key="users.id", nullable=False)
    user_2: int = Field(foreign_key="users.id", nullable=False)
    friends_since: date = Field(default_factory=date.today)
    
    # Relationships for complex self-referencing tables are often omitted or handled manually
    # user_a: User = Relationship(...)
    # user_b: User = Relationship(...)

# --------------------
# Auth Token
# --------------------
class Token(BaseModel):
    access_token: str
    token_type: str