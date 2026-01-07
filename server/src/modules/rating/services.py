from fastapi import HTTPException, status, Depends
from sqlmodel import Session, select, col

from src.modules.user.models import User
from src.modules.movies.models import Movie
from src.modules.rating.models import RatedMovie
from src.core.deps import get_session

class RatingOperations:
    def __init__(self, session: Session):
        self.session = session

    def add(
        self, 
        user: User, 
        movie_id: int, 
        rating_value: int
    ) -> RatedMovie:
        """Add new rating for a movie."""

        # Check if movie exists
        movie = self.session.get(Movie, movie_id)
        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with id {movie_id} not found."
            )

        # Check if user already rated this movie
        existing_rating = self.session.exec(
            select(RatedMovie)
            .where(RatedMovie.user_id == user['id'])
            .where(RatedMovie.movie_id == movie_id)
        ).first()

        if existing_rating:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already rated this movie. Use update instead."
            )

        new_rating = RatedMovie(user_id=user['id'], movie_id=movie_id, rating=rating_value)
        self.session.add(new_rating)
        self.session.commit()
        self.session.refresh(new_rating)
        return new_rating


    def remove(
        self, 
        user: User, 
        rating_id: int
    ) -> bool:
        """Delete a rating. Fails if the user is not the owner."""
        
        rating = self.get(rating_id)

        # Check ownership
        if rating.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this rating."
            )

        self.session.delete(rating)
        self.session.commit()
        return True


    def update(
        self, 
        user: User, 
        rating_id: int, 
        new_value: int
    ) -> RatedMovie:
        """Update an existing rating."""
        
        rating = self.get(rating_id)

        # Check ownership
        if rating.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this rating."
            )
        
        rating.rating = new_value
        
        self.session.add(rating)
        self.session.commit()
        self.session.refresh(rating)
        return rating


    def get(
        self, 
        rating_id: int
    ) -> RatedMovie:
        """Get one specific rating by ID."""

        rating = self.session.get(RatedMovie, rating_id)

        if not rating:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Rating with id {rating_id} not found."
            )
        return rating


    def get_all_for_user(
        self, 
        user_id: int
    ) -> list[RatedMovie]:
        """Get all ratings created by user ordered by newest."""

        return self.session.exec(
            select(RatedMovie)
            .where(RatedMovie.user_id == user_id)
            .order_by(col(RatedMovie.created_at).desc())
        ).all()


    def get_all_for_movie(
        self, 
        movie_id: int
    ) -> list[RatedMovie]:
        """Get all ratings for a movie."""

        return self.session.exec(
            select(RatedMovie).where(RatedMovie.movie_id == movie_id)
        ).all()
    

    def get_avg_rating(
        self, 
        movie_id: int
    ) -> float:
        """Get avg rating for a movie"""

        all_ratings_obj = self.get_all_for_movie(movie_id)
        ratings = [r.rating for r in all_ratings_obj]
        return round(sum(ratings) / len(ratings), 0) if ratings else 0


def get_rating_operations(session: Session = Depends(get_session)):
    return RatingOperations(session)