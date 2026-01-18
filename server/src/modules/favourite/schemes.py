from pydantic import BaseModel

from src.modules.movies.schemes import MovieResponse

class FavouriteListAdd(BaseModel):
    user_id: int
    movie_id: int

class FavouriteListRemove(BaseModel):
    user_id: int
    movie_id: int

class FavouriteListElement(BaseModel):
    movie: MovieResponse