# src/modules/user/routes.py

from fastapi import APIRouter, status
from src.modules.auth.deps import UserDep
from src.core.deps import SessionDep
from src.modules.rating.deps import RatingOperationsDep
from src.modules.reviews.deps import ReviewOperationsDep
from src.modules.follows.deps import FollowOperationsDep
from .deps import UserOperationsDep
from .schemas import UserResponse, UserProfileResponse


user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.get("/search")
def search_users_endpoint(username: str, user_ops: UserOperationsDep, limit: int = 5):
    test = user_ops.search_users(username)
    print(test)
    return user_ops.search_users(username)

@user_router.get("/{username}", status_code=status.HTTP_200_OK)
def get_user_profile(username: str, user_ops: UserOperationsDep, rating_ops: RatingOperationsDep, reviews_ops: ReviewOperationsDep, follow_ops: FollowOperationsDep):
    return user_ops.get_user(username, rating_ops, reviews_ops, follow_ops, )




# @user_router.put("/update_description", status_code=status.HTTP_200_OK)
# def update_user_description(db_session: SessionDep, user: UserDep, description: str):
#     user_operations = UserOperations()
#     return user_operations.set_description(db_session, user, description)