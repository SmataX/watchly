from typing import TYPE_CHECKING, Optional
from datetime import datetime, date
from pydantic import BaseModel
from fastapi import Form

if TYPE_CHECKING:
    from src.modules.rating.schemas import RatingResponse
    from src.modules.reviews.schemas import ReviewResponse

class UserResponse(BaseModel):
    username: str
    profile_path: Optional[str]
    description: Optional[str]
    created_at: datetime
    rated_movies: list["RatingResponse"] 
    reviews: list["ReviewResponse"]


class UserProfileResponse(BaseModel):
    username: str
    profile_path: Optional[str]
    description: Optional[str]
    member_since: date
    rated_movies: list['RatingResponse']
    avg_rating: float
    reviews: list['ReviewResponse']
    fav_genres: list[str]
    following: int
    followers: int

class TopContributor(BaseModel):
    user_id: int
    user: UserResponse
    reviews_count: int

class UserUpdateRequest(BaseModel):
    user_id: int = Form()
    username: Optional[str] = Form(None)
    email: Optional[str] = Form(None)
    description: Optional[str] = Form(None)



from src.modules.rating.schemas import RatingResponse
from src.modules.reviews.schemas import ReviewResponse

UserResponse.model_rebuild()