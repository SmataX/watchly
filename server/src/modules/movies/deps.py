from typing import Annotated
from fastapi import Depends
from .services import MovieOperations, get_movie_operations, GenreOperations, get_genre_operations

MoviesOperationsDep = Annotated[MovieOperations, Depends(get_movie_operations)]
GenresOperationsDep = Annotated[GenreOperations, Depends(get_genre_operations)]