# src/modules/auth/auth_operations.py

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlmodel import Session, select
from typing import Annotated
from jose import jwt, JWTError
from passlib.context import CryptContext
from src.common.models import User
from src.common.schemes import CreateUserForm
from src.settings import settings
from datetime import timedelta, datetime


ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def create_user(db_session: Session, form: CreateUserForm) -> None:
    user = User(
        username=form.username,
        email=form.email,
        password=bcrypt_context.hash(form.password),
    )

    db_session.add(user)
    db_session.commit()


def auth_user(username: str, password: str, db_session: Session):
    q = select(User).where(User.username == username)
    user = db_session.exec(q).first()

    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user


def login_for_access_token(form_data: OAuth2PasswordRequestForm, db_session: Session):
    user = auth_user(form_data.username, form_data.password, db_session)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    token = create_access_token(user.username, user.id, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        user_id = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
    