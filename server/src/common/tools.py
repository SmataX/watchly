import json
from sqlmodel import Session, select
from src.common.db import engine
from src.common.models import Movie
from src.common.schemes import AddMovieForm
from src.modules.movies.movies_operations import add_movie
from pathlib import Path

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
