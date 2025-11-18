# src/main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.common.db import create_db_and_tables
from src.modules.auth import auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)

@app.get("/")
async def root():
    return {"Hello": "World"}