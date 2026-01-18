from typing import Annotated
from fastapi import Depends
from .services import FavouriteListOperations, get_favourite_list_operations

FavouriteListOperationsDep = Annotated[FavouriteListOperations, Depends(get_favourite_list_operations)]