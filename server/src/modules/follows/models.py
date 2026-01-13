from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.modules.auth.models import User

class Follow(SQLModel, table=True):
    __tablename__ = "follows"

    user_id: int = Field(primary_key=True, nullable=False, foreign_key="users.id")
    follow_id: int = Field(primary_key=True, nullable=False, foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.now)

    follow_user: 'User' = Relationship(back_populates="follows")