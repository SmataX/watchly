from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel

# --------------------
# User Model
# --------------------
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    password: str = Field(nullable=False)
    profile_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)


# --------------------
# MovieDirector Link Table (Many-to-Many)
# --------------------
class MovieDirector(SQLModel, table=True):
    __tablename__ = "movie_directors" #

    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Added Foreign Keys
    movie_id: int = Field(foreign_key="movies.id")
    director_id: int = Field(foreign_key="directors.id") 


# --------------------
# Movie Model
# --------------------
class Movie(SQLModel, table=True):
    __tablename__ = "movies"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    description: str
    duration: int
    poster_url: Optional[str] = None
    release_date: datetime
    created_at: datetime = Field(default_factory=datetime.now)

    directors: List["Director"] = Relationship(
        back_populates="movies", 
        link_model=MovieDirector
    )


# --------------------
# Director Model
# --------------------
class Director(SQLModel, table=True):
    __tablename__ = "directors"

    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    surname: str
    picture_url: str
    created_at: datetime = Field(default_factory=datetime.now)

    movies: List["Movie"] = Relationship(
        back_populates="directors", 
        link_model=MovieDirector
    )


# --------------------
# Auth Token
# --------------------
class Token(BaseModel):
    access_token: str
    token_type: str