# src/modules/movies/routes.py

from fastapi import APIRouter, Query
from .models import Movie, Genre
from .schemes import MovieData
from src.modules.auth.deps import UserDep
from src.modules.rating.services import RatingOperations
from src.core.deps import SessionDep
from .services import MovieOperations, GenreOperations
from random import randint
from typing import Optional


movies_router = APIRouter(prefix="/movies", tags=["movies"])

@movies_router.get("", response_model=list[MovieData])
def get_movies(
    session: SessionDep, 
    skip: int = 0, 
    limit: int = 100,
    genre: Optional[list[str]] = Query(None),
    rating_min: float = 0,
    rating_max: float = 10,
    year_min: int = 1000, 
    year_max: int = 3000
):
    movies_service = MovieOperations()
    rating_service = RatingOperations()

    movie_list = movies_service.get_all_movies_where(
        db_session=session, 
        skip=skip, 
        limit=limit,
        genres=genre,
        rating_min=rating_min,
        rating_max=rating_max,
        year_min=year_min,
        year_max=year_max
    )

    final_list = []

    for movie in movie_list:
        avg_rating = rating_service.get_avg_rating(session, movie.id)
        
        genres_list = [g.genre.name for g in movie.genres] if hasattr(movie, 'genres') else []

        final_list.append(MovieData(
            id=movie.id, 
            title=movie.title, 
            poster_path=movie.poster_path, 
            release_date=movie.release_date, 
            global_rating=avg_rating, 
            friends_rating=avg_rating, 
            user_rating=avg_rating, 
            genres=genres_list, 
            duration=movie.duration, 
            overview=movie.overview
        ))

    return final_list


@movies_router.get("/random", response_model=list[MovieData])
def get_random(session: SessionDep, limit: int):
    movies_service = MovieOperations()

    movies = movies_service.get_random_movies(db_session=session, limit=limit)

    return movies

@movies_router.get("/genres", response_model=list[Genre])
def get_genres(session: SessionDep):
    return GenreOperations.get_all_genres(session)


@movies_router.get("/{id}", response_model=MovieData)
def get_by_id(id: int, session: SessionDep):
    movies_service = MovieOperations()
    rating_service = RatingOperations()

    movie = movies_service.get_movie(session, id) 
    avg_rating = rating_service.get_avg_rating(session, movie.id)
        
    genres_list = [g.genre.name for g in movie.genres] if hasattr(movie, 'genres') else []

    return MovieData(
            id=movie.id, 
            title=movie.title, 
            poster_path=movie.poster_path, 
            release_date=movie.release_date, 
            global_rating=avg_rating, 
            friends_rating=0, 
            user_rating=avg_rating, 
            genres=genres_list, 
            duration=movie.duration, 
            overview=movie.overview
        )