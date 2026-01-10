from fastapi import HTTPException, status, Depends
from sqlmodel import Session, select, col

from src.modules.user.models import User
from src.modules.movies.models import Movie
from src.core.deps import get_session

from .models import RatedMovie

class RatingOperations:
    def __init__(self, session: Session):
        self.session = session

    def add(self, rating: RatedMovie) -> RatedMovie:
        """Add new rating for a movie."""

        # Check if movie exists
        movie = self.session.get(Movie, rating.movie_id)
        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with id {rating.movie_id} not found."
            )

        # Check if user already rated this movie
        existing_rating = self.session.exec(
            select(RatedMovie)
            .where(RatedMovie.user_id == rating.user_id)
            .where(RatedMovie.movie_id == rating.movie_id)
        ).first()

        if existing_rating:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already rated this movie. Use update instead."
            )

        self.session.add(rating)
        self.session.commit()
        self.session.refresh(rating)
        return rating


    def get(self, id: int) -> RatedMovie:
        """Get one specific rating by ID."""

        rating = self.session.get(RatedMovie, id)

        if not rating:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Rating with id {id} not found."
            )
        return rating


    def get_all_for_user(self, user_id: int) -> list[RatedMovie]:
        """Get all ratings created by user ordered by newest."""

        return self.session.exec(
            select(RatedMovie)
            .where(RatedMovie.user_id == user_id)
            .order_by(col(RatedMovie.created_at).desc())
        ).all()


    def get_all_for_movie(self, movie_id: int) -> list[RatedMovie]:
        """Get all ratings for a movie."""

        return self.session.exec(
            select(RatedMovie).where(RatedMovie.movie_id == movie_id)
        ).all()
    

    def get_avg_rating(self, movie_id: int) -> float:
        """Get avg rating for a movie"""

        all_ratings_obj = self.get_all_for_movie(movie_id)
        ratings = [r.rating for r in all_ratings_obj]
        return round(sum(ratings) / len(ratings), 0) if ratings else 0


def get_rating_operations(session: Session = Depends(get_session)):
    return RatingOperations(session)