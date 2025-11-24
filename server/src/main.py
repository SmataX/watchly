import json
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlmodel import Session, select

from src.common.db import create_db_and_tables, engine 
from src.modules.auth import auth_router
from src.modules.movies import movies_router 
from src.common.schemes import AddMovieForm
from src.modules.movies.movies_operations import add_movie
from src.common.models import Movie

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
                
                with open("movies.json", "r", encoding="utf-8") as f:
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

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables first
    create_db_and_tables()
    # Then populate data
    init_movies_data()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(movies_router)