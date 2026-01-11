from typing import Optional

from fastapi import APIRouter, Query, Depends

from src.core.deps import SessionDep
from src.modules.auth.deps import UserDep, UserOptionalDep
from src.modules.rating.deps import RatingOperationsDep
from src.modules.rating.schemas import RatingResponse
from src.modules.reviews.deps import ReviewOperationsDep
from src.modules.reviews.models import Review
from src.modules.reviews.schemas import ReviewResponse

from .models import Movie, Genre
from .schemes import MovieData, MovieResponse
from .services import GenreOperations
from .deps import MoviesOperationsDep, GenresOperationsDep


router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("/genres", response_model=list[Genre])
def get_genres(genre_ops: GenresOperationsDep):
    return genre_ops.get_all_genres()

@router.get("", response_model=list[MovieData])
def get_movies(
    movie_operations: MoviesOperationsDep,
    rating_ops: RatingOperationsDep,
    user: UserOptionalDep,
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

    data = []
    for movie in movies_list:
        user_rating = None
        friends_rating = None

        if user:
            user_rating = rating_ops.get_user_rating(movie.id, user['id']) or 0
        
        data.append({
            "movie": movie, 
            "avg_rating": rating_ops.get_avg_rating(movie.id), 
            "friends_rating": friends_rating, 
            "user_rating": user_rating
        })

    return data


@router.get("/random", response_model=list[MovieResponse])
def get_random(limit: int, movie_operations: MoviesOperationsDep):
    return movie_operations.get_random_movies(limit=limit)

@router.get("/search", response_model=list[MovieResponse])
def search_movies_endpoint(
    title: str, 
    movie_operations: MoviesOperationsDep, 
    limit: int = 5
):
    return movie_operations.search_movies(title, limit)

@router.get("/{id}", response_model=MovieResponse)
def get_by_id(id: int, movie_operations: MoviesOperationsDep, ):
    return movie_operations.get_movie(id)


@router.get("/{id}/genres", response_model=list[Genre])
def get_genres(id: int, genres_ops: GenresOperationsDep):
    return genres_ops.get_all_genres_for_movie(id)


@router.get("/{id}/reviews", response_model=list[ReviewResponse])
def get_reviews(id: int, review_ops: ReviewOperationsDep):
    return review_ops.get_all_for_movie(id)


@router.get("/{id}/rating", response_model=float)
def get_avg_rating(id: int, rating_ops: RatingOperationsDep):
    return rating_ops.get_avg_rating(id)


@router.get("/{id}/user_rating", response_model=Optional[float])
def get_user_rating(id: int, user: UserDep, rating_ops: RatingOperationsDep):
    return rating_ops.get_user_rating(id, user['id'])


@router.get("/{id}/friends_rating", response_model=float)
def get_firends_rating(id: int, user: UserDep, rating_ops: RatingOperationsDep):
    return 0