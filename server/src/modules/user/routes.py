# src/modules/user/routes.py

from fastapi import APIRouter, status
from src.modules.auth.deps import UserDep
from src.common.db import SessionDep
from src.modules.user.user_operations import UserOperations


user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.get("/{username}", status_code=status.HTTP_200_OK)
def get_user_profile(db_session: SessionDep, username: str):
    user_operations = UserOperations()
    return user_operations.get_user_details(db_session, username)


@user_router.put("/update_description", status_code=status.HTTP_200_OK)
def update_user_description(db_session: SessionDep, user: UserDep, description: str):
    user_operations = UserOperations()
    return user_operations.set_description(db_session, user, description)