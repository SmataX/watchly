from datetime import datetime, date
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from src.modules.auth.models import User
from src.modules.movies.models import Movie

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

