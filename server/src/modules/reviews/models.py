from datetime import datetime, date
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel

from typing import Optional
from datetime import datetime, date
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from src.modules.user.models import User
    from src.modules.movies.models import Movie


class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    id: Optional[int] = Field(default=None, primary_key=True)
    movie_id: int = Field(nullable=False, foreign_key="movies.id")
    user_id: int = Field(nullable=False, foreign_key="users.id")
    content: str = Field()
    created_at: datetime = Field(default_factory=datetime.now)

    user: "User" = Relationship(back_populates="reviews")
    movie: "Movie" = Relationship(back_populates="reviews")
