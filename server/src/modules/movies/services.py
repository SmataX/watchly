# src/modules/movies/movies_operations.py

from fastapi import HTTPException, status
from sqlmodel import Session, select, func
from .schemes import MovieData
from .models import Movie, Genre


class MovieOperations:
    @staticmethod
    def get_all_movies(db_session: Session, skip: int = 0, limit: int = 100) -> list[Movie]:
        """Retrieves all movies with pagination."""

        return db_session.exec(
            select(Movie).offset(skip).limit(limit)
        ).all()
    
    @staticmethod
    def get_all_movies_where(db_session: Session, skip: int = 0, limit: int = 100) -> list[Movie]:
        pass

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
            genres=[],
            duration=movie.duration,
            overview=movie.overview
        )
        
        return movie_data


class GenreOperations:
    def get_all_genres(db_session: Session) -> list[Genre]:
        return db_session.exec(select(Genre))

    def get_all_genres_for_movie(db_session: Session, movie_id: int) -> list[Genre]:
        pass