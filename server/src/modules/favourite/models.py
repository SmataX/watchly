from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.movies.models import Movie


class Favourite(SQLModel, table=True):
    __tablename__ = "favourite_list"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    movie_id: int = Field(foreign_key="movies.id")
    created_at: datetime = Field(default_factory=datetime.now)

    movie: "Movie" = Relationship()