from sqlmodel import SQLModel, Field
from datetime import datetime

class RatingCreate(SQLModel):
    movie_id: int
    rating: int = Field(ge=1, le=5, description="Value between 1 and 5")


class RatingUpdate(SQLModel):
    rating: int = Field(ge=1, le=5)


class RatingRead(SQLModel):
    id: int
    movie_id: int
    user_id: int
    rating: int
    created_at: datetime