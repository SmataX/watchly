from fastapi import APIRouter
from src.modules.auth.deps import UserDep


from .schemas import ReviewCreateForm, ReviewGetForm, ReviewResponse, ReviewUpdateForm
from .deps import ReviewOperationsDep
from .models import Review


router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post('/', response_model=ReviewResponse)
def add(review_ops: ReviewOperationsDep, user: UserDep, form: ReviewCreateForm) -> ReviewResponse:
    review = Review(
        user_id=user['id'],
        movie_id=form.movie_id,
        content=form.content
        )
    
    return review_ops.add(review)


@router.put('/{review_id}', response_model=ReviewResponse)
def update(
    review_id: int, 
    review_ops: ReviewOperationsDep, 
    user: UserDep, 
    form: ReviewUpdateForm
):
    return review_ops.update(review_id, user['id'], form.content)


@router.delete('/')
def delete(review_ops: ReviewOperationsDep, user: UserDep, form: ReviewGetForm):
    return review_ops.remove(form.id, user['id'])