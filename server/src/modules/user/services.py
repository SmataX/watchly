# src/modules/user/user_operations.py

from fastapi import HTTPException, status
from sqlmodel import Session, select, func
from src.modules.auth.models import User
from src.modules.auth.deps import UserDep

class UserOperations:
    def get_user_by_id(self, db_session: Session, user_id: int):
        """Retrieves a user by their ID."""

        user = db_session.get(User, user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"User with id {user_id} not found."
            )
        return user
    

    def get_user_by_username(self, db_session: Session, username: str):
        """Retrieves a user by their username."""
        user = db_session.exec(select(User).where(User.username==username)).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"User with username {username} not found."
            )
        return user


    def get_user_details(self, db_session: Session, username: str):
        """Retrieves detailed information about a user by their ID."""

        from src.modules.rating.services import RatingOperations
        from src.modules.movies.services import MovieOperations

        rating_operations = RatingOperations()

        user_data = self.get_user_by_username(db_session, username)

        ratings = rating_operations.get_all_for_user(db_session, user_data.id)
        rated_movies = []
        rating_values = []

        for rating in ratings:
            movie = MovieOperations.get_movie(db_session, rating.movie_id)
            rated_movies.append(
                {"title": movie.title, "poster_path": movie.poster_path, "rating": rating.rating}
            )
            rating_values.append(rating.rating)

        avg_rating = round(sum(rating_values) / len(rating_values), 2) if rating_values else 0
        
        return {
            'id': user_data.id, 
            'username': user_data.username, 
            'description': user_data.description, 
            'profile_path': user_data.profile_path, 
            'created_at': user_data.created_at.date(), 
            'rated_movies': rated_movies,
            'avg_rating': avg_rating,
            'reviews': [],
            'following': 0,
            'followers': 0
        }
    

    def set_description(self, db_session: Session, user: UserDep, description: str):
        """Sets the description for a user."""
        u = self.get_user_by_id(db_session, user['id'])
        u.description = description
        db_session.add(u)
        db_session.commit()
        db_session.refresh(u)
        return u