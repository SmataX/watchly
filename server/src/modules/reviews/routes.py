from fastapi import APIRouter
from src.modules.auth.deps import UserDep


from .schemas import ReviewCreate
from .deps import ReviewOperationsDep
from .models import Review



router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post('/', response_model=Review)
def add(review_operations: ReviewOperationsDep, user: UserDep, form: ReviewCreate) -> Review:
    review = Review(
        user_id=user['id'],
        movie_id=form.movie_id,
        content=form.content
        )
    
    return review_operations.add(review)


@router.delete('/')
def delete():
    pass