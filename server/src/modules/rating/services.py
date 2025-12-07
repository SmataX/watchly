from fastapi import HTTPException, status
from sqlmodel import Session, select, col

from src.modules.user.models import User
from src.modules.movies.models import Movie
from src.modules.rating.models import RatedMovie

class RatingOperations:
    def add(self, db_session: Session, user: User, movie_id: int, rating_value: int) -> RatedMovie:
        """Add new rating for a movie."""

        # Check if movie exists
        movie = db_session.get(Movie, movie_id)
        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Movie with id {movie_id} not found."
            )

        # Check if user already rated this movie
        existing_rating = db_session.exec(
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
        db_session.add(new_rating)
        db_session.commit()
        db_session.refresh(new_rating)
        return new_rating


    def remove(self, db_session: Session, user: User, rating_id: int) -> bool:
        """Delete a rating. Fails if the user is not the owner."""
        
        rating = self.get(db_session, rating_id)

        # Check ownership
        if rating.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this rating."
            )

        db_session.delete(rating)
        db_session.commit()
        return True


    def update(self, db_session: Session, user: User, rating_id: int, new_value: int) -> RatedMovie:
        """Update an existing rating."""
        
        rating = self.get(db_session, rating_id)

        # Check ownership
        if rating.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this rating."
            )
        
        rating.rating = new_value
        
        db_session.add(rating)
        db_session.commit()
        db_session.refresh(rating)
        return rating


    def get(self, db_session: Session, rating_id: int) -> RatedMovie:
        """Get one specific rating by ID."""

        rating = db_session.get(RatedMovie, rating_id)

        if not rating:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Rating with id {rating_id} not found."
            )
        return rating


    def get_all_for_user(self, db_session: Session, user_id: int) -> list[RatedMovie]:
        """Get all ratings created by user ordered by newest."""

        return db_session.exec(
            select(RatedMovie)
            .where(RatedMovie.user_id == user_id)
            .order_by(col(RatedMovie.created_at).desc())
        ).all()


    def get_all_for_movie(self, db_session: Session, movie_id: int) -> list[RatedMovie]:
        """Get all ratings for a movie."""

        return db_session.exec(
            select(RatedMovie).where(RatedMovie.movie_id == movie_id)
        ).all()