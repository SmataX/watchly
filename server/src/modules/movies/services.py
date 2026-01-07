# src/modules/movies/movies_operations.py

from fastapi import HTTPException, status
from sqlmodel import Session, select, func, extract
from typing import Optional
from .schemes import MovieData
from .models import Movie, Genre, MovieGenre
from src.modules.rating.models import RatedMovie


class MovieOperations:
    @staticmethod
    def get_all_movies(db_session: Session, skip: int = 0, limit: int = 100) -> list[Movie]:
        """Retrieves all movies with pagination."""

        return db_session.exec(
            select(Movie).offset(skip).limit(limit)
        ).all()
    

    @staticmethod
    def get_all_movies_where(
        db_session: Session, 
        skip: int = 0, 
        limit: int = 100, 
        genres: Optional[list[str]] = None, 
        rating_min: Optional[float] = 0, 
        rating_max: Optional[float] = 10, 
        year_min: Optional[int] = 1000, 
        year_max: Optional[int] = 3000
    ) -> list[Movie]:

        query = select(Movie)
        print(genres)

        if year_min is not None:
            query = query.filter(extract("year", Movie.release_date) >= year_min)
        if year_max is not None:
            query = query.filter(extract("year", Movie.release_date) <= year_max)

        if genres:
            query = query.join(MovieGenre, Movie.id == MovieGenre.movie_id)
            query = query.join(Genre, MovieGenre.genre_id == Genre.id)
            query = query.where(Genre.name.in_(genres))

        if rating_min > 0 or rating_max < 10:
            query = query.outerjoin(RatedMovie, Movie.id == RatedMovie.movie_id)
            query = query.group_by(Movie.id)
            
            avg_rating = func.coalesce(func.avg(RatedMovie.rating), 0)
            
            if rating_min is not None:
                query = query.having(avg_rating >= rating_min)
            if rating_max is not None:
                query = query.having(avg_rating <= rating_max)
        
        elif genres:
            query = query.distinct()

        return db_session.exec(query.offset(skip).limit(limit)).all()
    

    @staticmethod
    def get_random_movies(db_session: Session, limit: int = 100) -> list[Movie]:
        """Retrives a random selection of movies."""

        return db_session.exec(
            select(Movie).order_by(func.random()).limit(limit)
        )

    @staticmethod
    def get_movie(db_session: Session, movie_id: int) -> Movie:
        """Retrieves a movie by its ID."""

        movie = db_session.get(Movie, movie_id)

        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Movie with id {movie_id} not found."
            )
        return movie
    
    @staticmethod
    def convert_to_movie_data(db_session: Session, movie: Movie) -> MovieData:

        movie_data = MovieData(
            id=movie.id,
            title=movie.title,
            poster_path=movie.poster_path,
            release_date=movie.release_date,
            global_rating=0,
            friends_rating=0,
            user_rating=0,
            genres=[g.name for g in GenreOperations.get_all_genres_for_movie(movie.id)],
            duration=movie.duration,
            overview=movie.overview
        )
        
        return movie_data


class GenreOperations:
    @staticmethod
    def get_all_genres(db_session: Session) -> list[Genre]:
        return db_session.exec(select(Genre)).all()

    @staticmethod
    def get_all_genres_for_movie(db_session: Session, movie_id: int) -> list[Genre]:
        statement = (
            select(Genre)
            .join(MovieGenre, Genre.id == MovieGenre.genre_id)
            .where(MovieGenre.movie_id == 1)
        )

        return db_session.exec(statement).all()