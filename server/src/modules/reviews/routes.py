# src/modules/movies/routes.py

from fastapi import APIRouter

router = APIRouter(prefix="/movies", tags=["movies"])