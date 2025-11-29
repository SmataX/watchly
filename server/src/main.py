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
from src.common.tools import init_movies_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    init_movies_data()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(movies_router)