from typing import Annotated
from fastapi import Depends
from .services import UserOperations, get_user_operations

UserOperationsDep = Annotated[UserOperations, Depends(get_user_operations)]