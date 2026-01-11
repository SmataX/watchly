from typing import Annotated
from fastapi import Depends
from .services import ReviewOperations, get_review_operations

ReviewOperationsDep = Annotated[ReviewOperations, Depends(get_review_operations)]