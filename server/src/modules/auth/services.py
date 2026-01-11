# src/modules/auth/auth_operations.py

from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional, Dict, Any

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from .models import User
from .schemes import RegisterUserScheme
from src.core.config import config


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_user(db_session: Session, form: RegisterUserScheme) -> User:
    user = User(
        username=form.username,
        email=form.email,
        password=bcrypt_context.hash(form.password),
    )

    db_session.add(user)

    try:
        db_session.commit()
        db_session.refresh(user)
        return user
    except IntegrityError:
        db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email or username already exists."
        )


def authenticate_user(username: str, password: str, db_session: Session) -> Optional[User]:
    q = select(User).where(User.username == username)
    user = db_session.exec(q).first()

    if not user:
        return None
    
    if not bcrypt_context.verify(password, user.password):
        return None
        
    return user


def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"sub": username, "id": user_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


def login_for_access_token(form_data: OAuth2PasswordRequestForm, db_session: Session) -> Dict[str, str]:
    user = authenticate_user(form_data.username, form_data.password, db_session)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = create_access_token(
        username=user.username, 
        user_id=user.id, 
        expires_delta=timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {'access_token': token, 'token_type': 'bearer'}


async def get_token(request: Request) -> Optional[str]:
    cookie_token = request.cookies.get("access_token")
    if cookie_token:
        if " " in cookie_token:
            return cookie_token.split(" ")[1]
        return cookie_token

    header_token = request.headers.get("Authorization")
    if header_token:
        scheme, _, param = header_token.partition(" ")
        if scheme.lower() == "bearer":
            return param
            
    return None


async def get_current_user(token: Annotated[Optional[str], Depends(get_token)]) -> Dict[str, Any]:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not token:
        raise credentials_exception
    
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        
        if username is None or user_id is None:
            raise credentials_exception
            
        return {'username': username, 'id': user_id}
        
    except JWTError:
        raise credentials_exception
    

async def get_optional_user(token: Annotated[Optional[str], Depends(get_token)]) -> Optional[Dict[str, Any]]:
    if not token:
        return None
    
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        return {'username': payload.get('sub'), 'id': payload.get('id')}
    except JWTError:
        return None