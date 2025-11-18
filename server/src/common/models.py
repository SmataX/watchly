# src/common/models.py

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
# Auth Token
# --------------------
class Token(BaseModel):
    access_token: str
    token_type: str