from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class UserFollow(SQLModel, table=True):
    __tablename__ = "user_follows"

    follower_id: int | None = Field(default=None, foreign_key="users.id", primary_key=True)
    followed_id: int | None = Field(default=None, foreign_key="users.id", primary_key=True)
    follow_since: datetime = Field(default_factory=datetime.now)