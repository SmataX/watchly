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
    token = request.cookies.get("access_token")
    token = token.split(' ')[1] if token else None

    data = await get_data(f"/movies?{request.url.query}" if request.url.query else "/movies", client, token)
    genres_list = await get_data("/movies/genres", client)

    return templates.TemplateResponse("all_movies.html", {
        "request": request, 
        "data": data,
        "genres": genres_list,
        "user": user,
        "filters": request.query_params
    })


@router.get("/{movie_id}")
async def movie_detail(
    movie_id: int, 
    request: Request, 
    client: httpx.AsyncClient = Depends(get_http_client), 
    user: Optional[dict] = Depends(get_optional_user),
):
    token = request.cookies.get("access_token")
    token = token.split(' ')[1] if token else None

    movie = await get_data(f"http://127.0.0.1:8001/movies/{movie_id}", client)
    reviews = await get_data(f"http://127.0.0.1:8001/movies/{movie_id}/reviews", client)
    avg_rating = await get_data(f"http://127.0.0.1:8001/movies/{movie_id}/rating", client)
    user_rating = await get_data(f"http://127.0.0.1:8001/movies/{movie_id}/user_rating", client, token)
    friends_rating = await get_data(f"http://127.0.0.1:8001/movies/{movie_id}/friends_rating", client, token)
    

    if not movie:
        pass    # Redirect to Not Found page

    return templates.TemplateResponse("movie_page.html", {
        "request": request, 
        "movie": movie,
        "user": user,
        "reviews": reviews,
        "avg_rating": avg_rating,
        "user_rating": user_rating,
        "friends_rating": friends_rating
    })