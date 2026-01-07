from typing import Optional

from fastapi import HTTPException, status, Depends
from sqlmodel import Session, select, func, extract

from src.core.deps import get_session
from src.modules.rating.models import RatedMovie
from src.modules.rating.services import RatingOperations

from .schemes import MovieData
from .models import Movie, Genre, MovieGenre


class MovieOperations:
    def __init__(self, session: Session):
        self.session = session
        self.rating_operations = RatingOperations(session)

    def get_all_movies(self, skip: int = 0, limit: int = 100) -> list[Movie]:
        """Retrieves all movies with pagination."""

        return self.session.exec(
            select(Movie).offset(skip).limit(limit)
        ).all()
    

    def get_all_movies_where(
        self,
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

        return self.session.exec(query.offset(skip).limit(limit)).all()
    

    def get_random_movies(self, limit: int = 100) -> list[Movie]:
        """Retrives a random selection of movies."""

        return self.session.exec(
            select(Movie).order_by(func.random()).limit(limit)
        )


    def get_movie(self, movie_id: int) -> Movie:
        """Retrieves a movie by its ID."""

        movie = self.session.get(Movie, movie_id)

        if not movie:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Movie with id {movie_id} not found."
            )
        return movie
    

    def get_full_data(
        self, 
        movie: Movie,
    ) -> MovieData:
        avg_rating = self.rating_operations.get_avg_rating(movie.id)
        genres_list = [g.genre.name for g in movie.genres] if hasattr(movie, 'genres') else []

        movie_data = MovieData(
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
        )
        
        return movie_data
    
def get_movie_operations(session: Session = Depends(get_session)):
    return MovieOperations(session)


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
    


