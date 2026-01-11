from fastapi import APIRouter, status
from src.core.deps import SessionDep
from src.modules.auth.deps import UserDep
from src.modules.rating.schemas import RatingCreateForm, RatingUpdateForm, RatingGetForm, RatingResponse
from src.modules.rating.deps import RatingOperationsDep
from .models import RatedMovie


router = APIRouter(prefix="/rating", tags=["Rating"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def set_rating(user: UserDep, rating_operations: RatingOperationsDep, form: RatingCreateForm, ):
    """Add a new rating."""
    rating = RatedMovie(
        user_id=user['id'],
        movie_id=form.movie_id,
        rating=form.rating
    )
    return rating_operations.add(rating)


# @router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
# def clear_rating(user: UserDep, rating_operations: RatingOperationsDep, form: RatingGetForm):
#     """Remove a rating by its ID."""

#     rating_operations.remove(db_session=session, user=user, rating_id=rating_id)
#     return None