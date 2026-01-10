from pydantic import BaseModel

class ReviewCreate(BaseModel):
    movie_id: int
    content: str

class ReviewGet(BaseModel):
    review_id: int