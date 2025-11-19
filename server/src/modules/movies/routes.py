# src/modules/movies/routes.py

from fastapi import APIRouter, status
from src.common.models import Movie
from src.common.schemes import AddMovieForm
from src.common.deps import SessionDep, UserDep
from src.modules.movies.movies_operations import add_movie, get_all_movies, get_movie_by_id, update_movie, delete_movie


movies_router = APIRouter(prefix="/movies", tags=["movies"])

@movies_router.get("", response_model=list[Movie])
def get_all(session: SessionDep, skip: int = 0, limit: int = 100):
    return get_all_movies(session, skip, limit)


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