# src/modules/auth/auth_operations.py

from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional, Dict, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from src.common.models import User
from src.common.schemes import CreateUserForm
from src.settings import settings

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def create_user(db_session: Session, form: CreateUserForm) -> User:
    """
    Creates a new user in the database.
    
    Hashes the password before storage and handles uniqueness constraints
    (e.g., duplicate username or email) by raising a 400 Bad Request error.

    Args:
        db_session (Session): The active database session.
        form (CreateUserForm): The Pydantic model containing registration data.

    Returns:
        User: The newly created User object.

    Raises:
        HTTPException: If the email or username already exists.
    """
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
    """
    Verifies a user's credentials against the database.

    Args:
        username (str): The username to look up.
        password (str): The plain-text password to verify.
        db_session (Session): The active database session.

    Returns:
        Optional[User]: The User object if credentials are valid, otherwise None.
    """
    q = select(User).where(User.username == username)
    user = db_session.exec(q).first()

    if not user:
        return None
    
    if not bcrypt_context.verify(password, user.password):
        return None
        
    return user


def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    """
    Generates a JWT access token.

    Args:
        username (str): The subject of the token (sub).
        user_id (int): Custom claim for user ID.
        expires_delta (Optional[timedelta]): How long the token is valid. 
                                            Defaults to 30 minutes if None.

    Returns:
        str: The encoded JWT string.
    """
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"sub": username, "id": user_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def login_for_access_token(form_data: OAuth2PasswordRequestForm, db_session: Session) -> Dict[str, str]:
    """
    Orchestrates the login process.

    Authenticates the user using form data and issues a JWT token if successful.

    Args:
        form_data (OAuth2PasswordRequestForm): FastAPI standard login form.
        db_session (Session): The active database session.

    Returns:
        Dict[str, str]: A dictionary containing the access token and token type.

    Raises:
        HTTPException: If authentication fails (401).
    """
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
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {'access_token': token, 'token_type': 'bearer'}


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> Dict[str, Any]:
    """
    Decodes and validates the JWT token to retrieve the current user's identity.

    Note: This does not hit the database, making it fast but stateless.
    If you need to ensure the user hasn't been deleted since the token was issued,
    you should add a database query here.

    Args:
        token (str): The JWT token from the Authorization header.

    Returns:
        Dict[str, Any]: A dictionary containing the user's username and ID.

    Raises:
        HTTPException: If the token is invalid or expired (401).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        
        if username is None or user_id is None:
            raise credentials_exception
            
        return {'username': username, 'id': user_id}
        
    except JWTError:
        raise credentials_exception