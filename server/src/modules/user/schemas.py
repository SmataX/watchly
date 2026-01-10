from typing import TYPE_CHECKING, Optional
from datetime import datetime
from pydantic import BaseModel

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


from src.modules.rating.schemas import RatingResponse
from src.modules.reviews.schemas import ReviewResponse

UserResponse.model_rebuild()