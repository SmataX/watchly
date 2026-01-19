from fastapi import Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.orm import joinedload

from src.core.db import Session
from src.core.deps import get_session
from src.modules.auth.services import get_current_user
from src.modules.auth.models import User
from src.modules.movies.models import Movie

from .models import Review
from .schemas import ReviewCreateForm

class ReviewOperations:
    def __init__(self, session: Session):
        self.session = session

    def add(self, review: Review) -> Review:

        # Check if user already write review for this movie
        q = select(Review).where(Review.movie_id == review.movie_id, Review.user_id == review.user_id)
        result = self.session.exec(q).first()

        if result:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You have already write review for this movie."
            )

        self.session.add(review)
        self.session.commit()
        self.session.refresh(review, ['user'])
        return review


    def remove(self, review_id: int, user_id: int) -> Review:
        review = self.get(review_id)

        if review_id == user_id:
            self.session.delete(review)
            self.session.commit()

        return review

    
    def update(self, review_id: int, user_id: int, new_content: str) -> Review:
        review = self.get(review_id)

        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Review not found."
            )

        if review.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only edit your own reviews."
            )

        review.content = new_content
        self.session.add(review)
        self.session.commit()
        self.session.refresh(review)
        return review


    def get(self, review_id: int) -> Review:
        return self.session.get(Review, review_id)


    def get_all_for_user(self, user_id: int) -> list[Review]:
        return self.session.exec(
            select(Review)
            .where(Review.user_id == user_id)
            .options(joinedload(Review.user), joinedload(Review.movie))
        ).unique().all()


    def get_all_for_movie(self, movie_id: int) -> list[Review]:
        return self.session.exec(
            select(Review).where(Review.movie_id==movie_id)
        ).all()
    

def get_review_operations(session: Session = Depends(get_session)):
    return ReviewOperations(session)
