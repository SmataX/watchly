# src/modules/movies/routes.py

from fastapi import APIRouter, status
from .models import Movie
from .schemes import AddMovieForm, MovieDataShort
from src.modules.auth.deps import UserDep
from src.modules.rating.services import RatingOperations
from src.core.deps import SessionDep
from .services import add_movie, get_all_movies, get_movie_by_id, update_movie, delete_movie, get_random_movies


movies_router = APIRouter(prefix="/movies", tags=["movies"])

@movies_router.get("/random", response_model=list[Movie])
def get_random(session: SessionDep, limit: int = 10):
    return get_random_movies(session, limit)

@movies_router.get("", response_model=list[MovieDataShort])
def get_all(session: SessionDep, skip: int = 0, limit: int = 100):
    rating_operations = RatingOperations()

    movie_list = get_all_movies(session, skip, limit)
    final_list = []

    for movie in movie_list:
        avg_rating = rating_operations.get_avg_rating(session, movie.id)
        final_list.append(MovieDataShort(id=movie.id, title=movie.title, poster_path=movie.poster_path, release_date=movie.release_date, rating=avg_rating))

    return final_list


@movies_router.get("/{id}", response_model=Movie)
def get_by_id(id: int, session: SessionDep):
    return get_movie_by_id(session, id)


@movies_router.post("", status_code=status.HTTP_201_CREATED, response_model=Movie)
def add(movie: AddMovieForm, session: SessionDep, user: UserDep):
    return add_movie(session, movie)


@movies_router.put("/{id}", response_model=Movie)
def update(id: int, movie: Movie, session: SessionDep, user: UserDep):
    return update_movie(session, id, movie)


@movies_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, session: SessionDep, user: UserDep):
    return delete_movie(session, id)