from fastapi import APIRouter, status
from src.core.deps import SessionDep
from src.modules.auth.deps import UserDep
from src.modules.rating.schemas import RatingCreate, RatingUpdate, RatingRead
from src.modules.rating.deps import RatingOperationsDep


router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/set_rating", status_code=status.HTTP_201_CREATED)
def set_rating(data: RatingCreate, session: SessionDep, user: UserDep, rating_operations: RatingOperationsDep):
    """Add a new rating."""

    return rating_operations.add(db_session=session, user=user, movie_id=data.movie_id, rating_value=data.rating)


@router.delete("/clear_rating/{rating_id}", status_code=status.HTTP_204_NO_CONTENT)
def clear_rating(session: SessionDep, user: UserDep, rating_id: int, rating_operations: RatingOperationsDep):
    """Remove a rating by its ID."""

    rating_operations.remove(db_session=session, user=user, rating_id=rating_id)
    return None


@router.put("/update_rating")
def update_rating(session: SessionDep, user: UserDep, rating_id: int, data: RatingUpdate, rating_operations: RatingOperationsDep):
    """Update an existing rating."""
    
    return rating_operations.update(db_session=session, user=user, rating_id=rating_id, new_value=data.rating)


@router.get("/get_rating/{rating_id}", response_model=RatingRead)
def get_rating(session: SessionDep, rating_id: int, rating_operations: RatingOperationsDep):
    """Get a specific rating by ID"""

    return rating_operations.get(db_session=session, rating_id=rating_id)


@router.get("/get_user_ratings/{user_id}", response_model=list[RatingRead])
def get_user_rating(session: SessionDep, user_id: int, rating_operations: RatingOperationsDep):
    """Get all ratings made by specific user."""

    return rating_operations.get_all_for_user(db_session=session, user_id=user_id)


@router.get("/get_movie_ratings/{movie_id}", response_model=list[RatingRead])
def get_movie_ratings(session: SessionDep, movie_id: int, rating_operations: RatingOperationsDep):
    """Get all ratings for a specific movie"""

    return rating_operations.get_all_for_movie(db_session=session, movie_id=movie_id)