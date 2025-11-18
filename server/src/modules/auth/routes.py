# src/modules/auth/routes.py

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from src.common.models import Token
from src.common.deps import SessionDep, UserDep
from src.common.schemes import CreateUserForm
from .auth_operations import create_user, login_for_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/")
def root(user: UserDep):
    if not user:
        return {"msg": "User not found"}
    return {"user": user}


@router.post("/register")
def register(db_session: SessionDep, form: CreateUserForm):
    create_user(db_session, form)
    return {"detail": "User created."}


@router.post("/login", response_model=Token)
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db_session: SessionDep):
    return login_for_access_token(form_data, db_session)








