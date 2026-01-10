from fastapi import Depends
from sqlmodel import select

from src.core.db import Session
from src.core.deps import get_session
from src.modules.auth.services import get_current_user
from src.modules.auth.models import User

from .models import Review
from .schemas import ReviewCreate

class ReviewOperations:
    def __init__(self, session: Session):
        self.session = session

    def add(self, review: Review) -> Review:
        self.session.add(review)
        self.session.commit()
        self.session.refresh(review)
        return review


    def remove(self, review_id: int, user: User = Depends(get_current_user)) -> Review:
        review = self.get(review_id)

        if not review:
            return
        
        if review.user_id != user['id']:
            return
        
        self.session.delete(review)
        self.session.commit()


    def get(self, review_id: int) -> Review:
        return self.session.get(Review, review_id)


    def get_all_for_user(self, user_id: int) -> list[Review]:
        return self.session.exec(
            select(Review).where(Review.user_id==user_id)
        ).all()


    def get_all_for_movie(self, movie_id: int) -> list[Review]:
        return self.session.exec(
            select(Review).where(Review.movie_id==movie_id)
        ).all()
    

def get_review_operations(session: Session = Depends(get_session)):
    return ReviewOperations(session)
