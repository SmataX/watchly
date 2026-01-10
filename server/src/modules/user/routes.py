# src/modules/user/routes.py

from fastapi import APIRouter, status
from src.modules.auth.deps import UserDep
from src.core.deps import SessionDep
from .deps import UserOperationsDep
from .schemas import UserResponse


user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.get("/{username}", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user_profile(username: str, user_ops: UserOperationsDep):
    return user_ops.get_user_by_username(username)




# @user_router.put("/update_description", status_code=status.HTTP_200_OK)
# def update_user_description(db_session: SessionDep, user: UserDep, description: str):
#     user_operations = UserOperations()
#     return user_operations.set_description(db_session, user, description)