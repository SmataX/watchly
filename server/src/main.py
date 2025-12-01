from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.common.db import create_db_and_tables 
from src.modules.movies.movies_operations import add_movie

from src.modules.auth import auth_router
from src.modules.movies import movies_router 
from src.modules.user import user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(movies_router)
app.include_router(user_router)