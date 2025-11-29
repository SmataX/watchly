# src/modules/movies/movies_operations.py

from fastapi import HTTPException, status
from sqlmodel import Session, select, func
import json
from pathlib import Path
from src.common.db import engine
from src.common.models import Movie
from src.common.schemes import AddMovieForm

def init_movies_data():
    """
    Checks if the Movie table is empty. 
    If so, loads data from movies.json and populates the database.
    """
    try:
        with Session(engine) as session:
            # Check if any movie exists in the database
            statement = select(Movie)
            result = session.exec(statement).first()

            if not result:
                print("Database is empty. Loading movies from JSON...")
                
                with open("../movies.json", "r", encoding="utf-8") as f:
                    movies_data = json.load(f)
                    
                    for movie_dict in movies_data:
                        # Create AddMovieForm instance
                        movie_form = AddMovieForm(**movie_dict)
                        # Use add_movie operation (handles commit internally)
                        add_movie(session, movie_form)
                    
                print("Movies loaded successfully.")
            else:
                print("Database already contains data. Skipping initialization.")
                
    except FileNotFoundError:
        # We now print the specific path it failed to find to help debugging
        current_dir = Path(__file__).resolve().parent
        print(f"Warning: 'movies.json' file not found at {current_dir / 'movies.json'}. Skipping data loading.")
    except Exception as e:
        print(f"An error occurred while loading movies: {e}")



def get_all_movies(db_session: Session, skip: int = 0, limit: int = 100):
    """Retrieves all movies with pagination."""
    return db_session.exec(
        select(Movie).offset(skip).limit(limit)
    ).all()


def get_movie_by_id(db_session: Session, id: int):
    """Retrieves a movie by its ID."""
    movie = db_session.get(Movie, id)

    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Movie with id {id} not found."
        )
    return movie


def add_movie(db_session: Session, form: AddMovieForm):
    """Adds a new movie to the database."""
    movie = Movie.model_validate(form)

    db_session.add(movie)
    db_session.commit()
    db_session.refresh(movie)
    return form


def update_movie(db_session: Session, id: int, data: Movie):
    """Updates a movie by its ID."""
    movie = get_movie_by_id(db_session, id)
    movie_data = data.model_dump(exclude_unset=True)
    
    movie.sqlmodel_update(movie_data)
    
    db_session.add(movie)
    db_session.commit()
    db_session.refresh(movie)
    
    return movie


def delete_movie(db_session: Session, id: int):
    """Deletes a movie by its ID."""
    movie = get_movie_by_id(db_session, id)
    
    db_session.delete(movie)
    db_session.commit()
    return True

def get_random_movies(db_session: Session, limit: int = 10):
    """Retrives a random selection of movies."""
    return db_session.exec(
        select(Movie).order_by(func.random()).limit(limit)
    )