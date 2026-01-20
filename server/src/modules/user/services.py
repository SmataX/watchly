from fastapi import HTTPException, status, Depends
from sqlmodel import Session, select, func, col
from sqlalchemy.orm import joinedload
from src.core.deps import get_session
from src.modules.auth.models import User
from src.modules.auth.deps import UserDep
from src.modules.rating.services import RatingOperations
from src.modules.rating.models import RatedMovie
from src.modules.reviews.models import Review
from src.modules.reviews.services import ReviewOperations
from src.modules.follows.services import FollowOperations
from src.modules.movies.models import Movie, MovieGenre, Genre

from .schemas import UserProfileResponse, TopContributor

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
    
    def search_users(self, username: str) -> list[User]:
        '''Searches for users by username.'''
        query = select(User).where(col(User.username).contains(username))
        return self.session.exec(query).all()

    def get_user_by_username(self, username: str) -> User:
        """Retrieves a user by their username."""
        user = self.session.exec(
            select(User).where(User.username == username)
        ).first()

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

    def update_username(self, user_id: int, username: str):
        query = select(User).where(User.username == username)
        existing_user = self.session.exec(query).first()


        if existing_user and existing_user.id != user_id:
            raise HTTPException(status_code=409, detail="Username is taken.")

        current_user = self.get_user_by_id(user_id)
        current_user.username = username

        self.session.add(current_user)
        self.session.commit()
        self.session.refresh(current_user)
        return current_user

    def update_email(self, user_id: int, email: str):
        try:
            current_user = self.get_user_by_id(user_id)
            current_user.email = email

            self.session.add(current_user)
            self.session.commit()
            self.session.refresh(current_user)
            return current_user
        except:
            raise HTTPException(status_code=409, detail="Username is taken.")
        

    def update_description(self, user_id: int, description: str):
        user = self.get_user_by_id(user_id)

        if not user:
            raise HTTPException(status_code=404, detail="Usern not found.")

        user.description = description
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user


    def get_user(self, username: str, rating_ops: RatingOperations, reviews_ops: ReviewOperations, follows_ops: FollowOperations):
        user = self.get_user_by_username(username)
        
        rated_movies = rating_ops.get_all_for_user(user.id)
        avg_rating = round(sum([x.rating for x in rated_movies]) / len(rated_movies), 2) if rated_movies else 0
        
        rated_movies_data = []
        for rating in rated_movies:
            r_dict = rating.model_dump()
            if rating.movie:
                r_dict["movie"] = rating.movie.model_dump()
            rated_movies_data.append(r_dict)

        reviews = reviews_ops.get_all_for_user(user.id)
        reviews_data = []
        for review in reviews:
            r_dict = review.model_dump()
            r_dict['created_at'] = r_dict['created_at'].date()
            if review.movie:
                r_dict["movie"] = review.movie.model_dump()
            reviews_data.append(r_dict)

        fav_genres = []
        following = len(follows_ops.get_all_follows(user.id))
        followers = len(follows_ops.get_all_followers(user.id))

        return {
            "username": user.username,
            "profile_path": user.profile_path,
            "description": user.description,
            "member_since": user.created_at.date(),
            "rated_movies": rated_movies_data,
            "avg_rating": avg_rating,
            "reviews": reviews_data,
            "fav_genres": fav_genres,
            "following": following,
            "followers": followers
        }

    
    def get_top_contributors(self, limit: int) -> list[TopContributor]:
        statement = (
            select(User, func.count(Review.id))
            .join(Review)
            .group_by(User)
            .order_by(func.count(Review.id).desc())
            .limit(limit)
        )
        
        results = self.session.exec(statement).all()
        
        return [{"user_id": user.id, "user": user, "reviews_count": count} for user, count in results]

    
def get_user_operations(session: Session = Depends(get_session)) -> UserOperations:
    return UserOperations(session)