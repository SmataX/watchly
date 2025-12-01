from typing import Annotated
from fastapi import Depends
from .auth_operations import get_current_user

UserDep = Annotated[dict, Depends(get_current_user)]