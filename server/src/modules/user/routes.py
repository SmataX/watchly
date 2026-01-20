# src/modules/user/routes.py

from fastapi import APIRouter, status, Form
from src.modules.auth.deps import UserDep
from src.core.deps import SessionDep
from src.modules.rating.deps import RatingOperationsDep
from src.modules.reviews.deps import ReviewOperationsDep
from src.modules.follows.deps import FollowOperationsDep
from src.modules.favourite.deps import FavouriteListOperationsDep
from .deps import UserOperationsDep
from .schemas import UserResponse, UserProfileResponse, TopContributor, UserUpdateRequest
from src.modules.favourite.schemes import FavouriteListElement
from typing import Optional


user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.patch("/update")
def update(
    user_ops: UserOperationsDep,
    user_id: int = Form(...),
    username: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    description: Optional[str] = Form(None)
):
    print('1')
    if username:
        print('2')
        user_ops.update_username(user_id, username)
        print('2-1')

    if email:
        print('3')
        user_ops.update_email(user_id, email)
    print('3-1')
    if description:
        print('4')
        user_ops.update_description(user_id, description)

    print('5')
    return {"status": "success"}

@user_router.get("/search")
def search_users_endpoint(username: str, user_ops: UserOperationsDep, limit: int = 5):
    test = user_ops.search_users(username)
    print(test)
    return user_ops.search_users(username)


@user_router.get("/top-contributors", response_model=list[TopContributor])
def get_top_contributors(user_ops: UserOperationsDep, limit: int = 5):
    return user_ops.get_top_contributors(limit)



@user_router.get("/{username}", status_code=status.HTTP_200_OK)
def get_user_profile(username: str, user_ops: UserOperationsDep, rating_ops: RatingOperationsDep, reviews_ops: ReviewOperationsDep, follow_ops: FollowOperationsDep):
    return user_ops.get_user(username, rating_ops, reviews_ops, follow_ops, )

@user_router.get("/{username}/fav", response_model=list[FavouriteListElement])
def get_fav_movies(fav_ops: FavouriteListOperationsDep, user_ops: UserOperationsDep, username: str, limit: int):
    return fav_ops.get_list(user_ops.get_user_by_username(username).id, limit)
