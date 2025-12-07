from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel

if TYPE_CHECKING:
    from src.modules.rating.models import Review, RatedMovie


# --------------------
# User Model
# --------------------
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    password: str = Field(nullable=False)
    profile_path: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.now)

    rated_movies: list["RatedMovie"] = Relationship(back_populates="user")
    # reviews: list["Review"] = Relationship(back_populates="user")


# --------------------
# Auth Token
# --------------------
class Token(BaseModel):
    access_token: str
    token_type: str