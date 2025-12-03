from datetime import datetime, date
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from src.modules.auth.models import User
from src.modules.movies.models import Movie


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

