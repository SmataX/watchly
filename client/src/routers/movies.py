import httpx

from typing import Optional

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse

from src.main import templates
from src.core.deps import get_optional_user, get_http_client
from src.core.utils import get_data


router = APIRouter(prefix="/movies")

@router.get("/")
async def movies(
    request: Request, 
    client: httpx.AsyncClient = Depends(get_http_client), 
    user: Optional[dict] = Depends(get_optional_user),
):
    movies_list = await get_data("/movies", client)
    genres_list = await get_data("/movies/genres", client)

    return templates.TemplateResponse("all_movies.html", {
        "request": request, 
        "movies": movies_list,
        "genres": genres_list,
        "user": user
    })


@router.get("/{movie_id}")
async def movie_detail(
    movie_id: int, 
    request: Request, 
    client: httpx.AsyncClient = Depends(get_http_client), 
    user: Optional[dict] = Depends(get_optional_user),
):
    movie = await get_data(f"http://127.0.0.1:8001/movies/{movie_id}", client)

    if not movie:
        pass    # Redirect to Not Found page

    return templates.TemplateResponse("movie_page.html", {
        "request": request, 
        "movie": movie,
        "user": user
    })