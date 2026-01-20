from fastapi import HTTPException, Depends
from sqlmodel import select, desc
from sqlalchemy.orm import selectinload

from src.core.db import Session
from src.core.deps import get_session
from src.modules.auth.deps import UserDep, UserOptionalDep

from .models import Favourite


class FavouriteListOperations:
    def __init__(self, session: Session):
        self.session = session

    def add(self, user_id: int, movie_id: int) -> Favourite:
        f = Favourite(user_id=user_id, movie_id=movie_id)
        self.session.add(f)
        self.session.commit()
        self.session.refresh(f)

    def remove(self, user_id: int, movie_id: int):
        fav_element = self.session.exec(
            select(Favourite).where(Favourite.user_id == user_id, Favourite.movie_id == movie_id)
        ).first()

        if fav_element:
            self.session.delete(fav_element)
            self.session.commit()

    def is_fav(self, user_id: int, movie_id: int):
        fav_element = self.session.exec(
            select(Favourite).where(Favourite.user_id == user_id, Favourite.movie_id == movie_id)
        ).first()

        if fav_element:
            return True
        return False

    def get_list(self, user_id: int, limit: int = 100) -> list[Favourite]:
        statement = (
            select(Favourite)
            .where(Favourite.user_id == user_id)
            .options(selectinload(Favourite.movie)).limit(limit)
            .order_by(Favourite.created_at.desc())
        )
        return self.session.exec(statement).all()


def get_favourite_list_operations(session: Session = Depends(get_session)) -> FavouriteListOperations:
    return FavouriteListOperations(session)
