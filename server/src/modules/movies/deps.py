from typing import Annotated
from fastapi import Depends
from .services import MovieOperations, get_movie_operations

MoviesOperationsDep = Annotated[MovieOperations, Depends(get_movie_operations)]