# src/common/deps.py

from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from src.common.db import get_session
from src.modules.auth.auth_operations import get_current_user



# SessionDep = Annotated[Session, Depends(get_session)]
# UserDep = Annotated[dict, Depends(get_current_user)]