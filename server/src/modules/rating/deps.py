from typing import Annotated
from fastapi import Depends
from .services import RatingOperations, get_rating_operations

RatingOperationsDep = Annotated[RatingOperations, Depends(get_rating_operations)]