from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.db import create_db_and_tables
from src.modules.auth import auth_router
from src.modules.user.routes import user_router

from src.modules.auth.models import *
from src.modules.movies.models import *
from src.modules.follows.models import *
from src.modules.reviews.models import *
from src.modules.favourite.models import *



origins = ["http://127.0.0.1:8000", "http://localhost:8000"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)

from src.modules.movies.routes import router as movies_router 
app.include_router(movies_router)

from src.modules.rating.routes import router as rating_router
app.include_router(rating_router)

from src.modules.reviews.routes import router as reviews_router
app.include_router(reviews_router)

from src.modules.follows.routes import router as follows_router
app.include_router(follows_router)