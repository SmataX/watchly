# src/modules/user/user_operations.py

from fastapi import HTTPException, status, Depends
from sqlmodel import Session, select, func
from sqlalchemy.orm import joinedload
from src.core.deps import get_session
from src.modules.auth.models import User
from src.modules.auth.deps import UserDep
from src.modules.rating.models import RatedMovie
from src.modules.reviews.models import Review
from src.modules.movies.models import Movie, MovieGenre, Genre

class UserOperations:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_id(self, user_id: int) -> User:
        """Retrieves a user by their ID."""

        user = self.session.get(User, user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"User with id {user_id} not found."
            )
        return user
    

    def get_user_by_username(self, username: str) -> User:
        """Retrieves a user by their username."""
        user = self.session.exec(
            select(User)
            .where(User.username == username)
            .options(
                joinedload(User.rated_movies),
                joinedload(User.reviews)
                .joinedload(Review.movie)
                .joinedload(Movie.genres)
                .joinedload(MovieGenre.genre) 
            )
        ).unique().first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        return user
    

    def set_description(self, db_session: Session, user: UserDep, description: str):
        """Sets the description for a user."""
        u = self.get_user_by_id(db_session, user['id'])
        u.description = description
        db_session.add(u)
        db_session.commit()
        db_session.refresh(u)
        return u
    
def get_user_operations(session: Session = Depends(get_session)) -> UserOperations:
    return UserOperations(session)