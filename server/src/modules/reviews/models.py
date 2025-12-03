from datetime import datetime, date
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel

from typing import Optional, List
from datetime import datetime, date
from sqlmodel import Field, SQLModel, Relationship

from src.modules.user.models import User
from src.modules.movies.models import Movie


class Rating(SQLModel, table=True):
    __tablename__ = "movies_ratings"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    movie_id: int = Field(foreign_key="movies.id")
    rating: int = Field(ge=1, le=10)
    created_at: datetime = Field(default_factory=datetime.now)

    user: "User" = Relationship(back_populates="movies_ratings")
    movie: "Movie" = Relationship(back_populates="movies_ratings")

class Review():
    pass