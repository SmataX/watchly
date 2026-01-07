from typing import Optional

from fastapi import APIRouter, Query, Depends

from src.core.deps import SessionDep
from src.modules.auth.deps import UserDep
from src.modules.rating.services import RatingOperations

from .models import Movie, Genre
from .schemes import MovieData
from .services import GenreOperations
from .deps import MoviesOperationsDep


movies_router = APIRouter(prefix="/movies", tags=["movies"])


@movies_router.get("", response_model=list[MovieData])
def get_movies(
    movie_operations: MoviesOperationsDep,
    skip: int = 0, 
    limit: int = 100,
    genre: Optional[list[str]] = Query(None),
    rating_min: float = 0,
    rating_max: float = 10,
    year_min: int = 1000, 
    year_max: int = 3000,
):
    movies_list = movie_operations.get_all_movies_where(
        skip=skip, 
        limit=limit,
        genres=genre,
        rating_min=rating_min,
        rating_max=rating_max,
        year_min=year_min,
        year_max=year_max
    )

    return [movie_operations.get_full_data(movie) for movie in movies_list]


@movies_router.get("/random", response_model=list[MovieData])
def get_random(limit: int, movie_operations: MoviesOperationsDep):
    movies = movie_operations.get_random_movies(limit=limit)
    return [movie_operations.get_full_data(movie) for movie in movies]


@movies_router.get("/genres", response_model=list[Genre])
def get_genres(session: SessionDep):
    return GenreOperations.get_all_genres(session)


@movies_router.get("/{id}", response_model=MovieData)
def get_by_id(id: int, movie_operations: MoviesOperationsDep, ):
    return movie_operations.get_full_data(movie_operations.get_movie(id) )