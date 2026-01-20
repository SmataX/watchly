from fastapi import HTTPException, Depends
from sqlmodel import select

from src.core.db import Session
from src.core.deps import get_session
from src.modules.auth.deps import UserDep, UserOptionalDep

from .models import UserFollow

class FollowOperations:
    def __init__(self, session: Session):
        self.session = session

    def add(self, user_id: int, follow_id: int) -> UserFollow:
        follow = UserFollow(follower_id=user_id, followed_id=follow_id)
        self.session.add(follow)
        self.session.commit()
        self.session.refresh(follow)
        return follow

    def remove(self, user_id: int, follow_id: int) -> UserFollow:
        result = self.session.exec(
            select(UserFollow).where(UserFollow.follower_id == user_id, UserFollow.followed_id == follow_id)
        ).first()

        self.session.delete(result)
        self.session.commit()
        return result
    
    def get_all_follows(self, user_id: int) -> list[UserFollow]:
        return self.session.exec(
            select(UserFollow).where(UserFollow.follower_id == user_id)
        ).all()

    def get_all_followers(self, user_id: int) -> list[UserFollow]:
        return self.session.exec(
            select(UserFollow).where(UserFollow.followed_id == user_id)
        ).all()

    def is_followed(self, user_id: int, followed_id: int) -> bool:
        return self.session.exec(
            select(UserFollow).where(UserFollow.follower_id==user_id, UserFollow.followed_id==followed_id)
        ).first() is not None
        
def get_follow_operations(session: Session = Depends(get_session)) -> FollowOperations:
    return FollowOperations(session)
