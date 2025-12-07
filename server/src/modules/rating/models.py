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

# --------------------
# Rated Movies
# --------------------
class RatedMovie(SQLModel, table=True):
    __tablename__ = "rated_movies"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    movie_id: int = Field(foreign_key="movies.id")
    rating: int = Field(ge=1, le=10)
    created_at: datetime = Field(default_factory=datetime.now)

    user: "User" = Relationship(back_populates="rated_movies")
    movie: "Movie" = Relationship(back_populates="ratings")