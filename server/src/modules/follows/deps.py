from typing import Annotated
from fastapi import Depends
from .services import get_follow_operations, FollowOperations

FollowOperationsDep = Annotated[FollowOperations, Depends(get_follow_operations)]