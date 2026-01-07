from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.core.db import create_db_and_tables

from src.modules.auth import auth_router
from src.modules.movies import movies_router 
from src.modules.user import user_router

from src.modules.rating.services import RatingOperations

from src.modules.auth.models import *
from src.modules.movies.models import *
from src.modules.user.models import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(movies_router)
app.include_router(user_router)

from src.modules.rating.routes import router as reviews_router
app.include_router(reviews_router)