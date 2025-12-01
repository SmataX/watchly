# src/modules/auth/routes.py

from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from src.common.models import Token
from src.common.schemes import CreateUserForm
from .auth_operations import create_user, login_for_access_token, get_current_user
from src.modules.auth.deps import UserDep
from src.common.db import SessionDep

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/")
def check_auth_status(user: UserDep):
    """
    Test endpoint to verify if the current user is authenticated.
    
    Args:
        user (UserDep): The authenticated user dependency.
        
    Returns:
        dict: The user object if authenticated.
    """
    # Note: If UserDep raises 401 on failure, this check is redundant.
    # If UserDep returns None on failure, this check is necessary.
    if not user:
        return {"msg": "User not found"}
    return {"user": user}


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(db_session: SessionDep, form: CreateUserForm):
    """
    Registers a new user.

    Args:
        db_session (SessionDep): Database session dependency.
        form (CreateUserForm): Registration form data (username, email, password).

    Returns:
        dict: Success message.
    """
    create_user(db_session, form)
    return {"detail": "User created successfully."}


@router.post("/login", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    db_session: SessionDep
):
    """
    Authenticates a user and returns an access token.

    Args:
        form_data (OAuth2PasswordRequestForm): FastAPI form containing username and password.
        db_session (SessionDep): Database session dependency.

    Returns:
        Token: The JWT access token and token type.
    """
    return login_for_access_token(form_data, db_session)


@router.get("/get-user")
def read_user_me(user_profile: Annotated[dict, Depends(get_current_user)]):
    """
    Retrieves the currently logged-in user's profile information.

    Args:
        user_profile (dict): The user profile returned by the auth dependency.

    Returns:
        dict: The user's profile data (id, username, etc.).
    """
    return user_profile