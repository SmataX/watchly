# src/modules/movies/routes.py

from fastapi import APIRouter
from .models import Movie
from .schemes import MovieData
from src.modules.auth.deps import UserDep
from src.modules.rating.services import RatingOperations
from src.core.deps import SessionDep
from .services import MovieOperations, GenreOperations
from random import randint


movies_router = APIRouter(prefix="/movies", tags=["movies"])


@movies_router.get("", response_model=list[MovieData])
def get_movies(session: SessionDep, skip: int = 0, limit: int = 100):
    movies_service = MovieOperations()
    rating_service = RatingOperations()

    movie_list = movies_service.get_all_movies(session, skip, limit)
    final_list = []

    for movie in movie_list:
        genres = []

        avg_rating = rating_service.get_avg_rating(session, movie.id)
        final_list.append(MovieData(id=movie.id, title=movie.title, poster_path=movie.poster_path, release_date=movie.release_date, global_rating=avg_rating, friends_rating=avg_rating, user_rating=avg_rating, genres=genres, duration=movie.duration, overview=movie.overview))

    return final_list


@movies_router.get("/random", response_model=list[MovieData])
def get_random(session: SessionDep, limit: int):
    movies_service = MovieOperations()

    movies = movies_service.get_random_movies(db_session=session, limit=limit)

    return movies


@movies_router.get("/{id}", response_model=Movie)
def get_by_id(id: int, session: SessionDep):
    movies_service = MovieOperations()

    return movies_service.get_movie(session, id)