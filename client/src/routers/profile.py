
from fastapi.responses import HTMLResponse
import httpx

from typing import Optional

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse

from src.main import templates
from src.core.deps import get_optional_user, get_http_client
from src.core.utils import get_data


router = APIRouter(prefix="/profile")


@router.get("/")
async def user_profile(
    request: Request, 
    user: Optional[dict] = Depends(get_optional_user),
    client: httpx.AsyncClient = Depends(get_http_client),
):
    if not user:
        return RedirectResponse("http://127.0.0.1:8001/login")
    
    user_data = await get_data(f"/user/{user['username']}", client)
    fav_movies = await get_data(f"http://127.0.0.1:8001/user/{user['username']}/fav?limit=8", client)

    return templates.TemplateResponse("profile.html", {
        "request": request, 
        "user": user,
        "user_data": user_data,
        "fav_movies": fav_movies,
    })


@router.get("/{username}/favorites")
async def user_favorites(
    username: str,
    request: Request, 
    client: httpx.AsyncClient = Depends(get_http_client),
    user: Optional[dict] = Depends(get_optional_user),
):
    
    token = request.cookies.get("access_token")
    token = token.split(' ')[1] if token else None
    fav_movies = await get_data(f"http://127.0.0.1:8001/user/{username}/fav?limit=100", client)
    
    return templates.TemplateResponse("favorite_movies.html", {
        "request": request,
        "user": user,
        "profile_username": username,
        "data": fav_movies if fav_movies else []
    })




@router.get("/edit", response_class=HTMLResponse)
async def edit_profile_page(
    request: Request,
    user: Optional[dict] = Depends(get_optional_user)
):
    if not user:
        return RedirectResponse(url="/login") 

    return templates.TemplateResponse("edit_profile.html", {
        "request": request,
        "user": user
    })

@router.get("/{username}")
async def user_profile(
    request: Request, 
    user: Optional[dict] = Depends(get_optional_user),
    client: httpx.AsyncClient = Depends(get_http_client),
    username: str = ""
):
    token = request.cookies.get("access_token")
    token = token.split(' ')[1] if token else None
    user_data = await get_data(f"http://127.0.0.1:8001/user/{username}", client)
    following = False
    fav_movies = await get_data(f"http://127.0.0.1:8001/user/{username}/fav?limit=8", client)
    if user:
        if user['username'] != username:
            following = await get_data(f"http://127.0.0.1:8001/follow/follow/{username}", client, token)
    return templates.TemplateResponse("profile.html", {
        "request": request, 
        "user": user,
        "following": following,
        "user_data": user_data,
        "fav_movies": fav_movies if fav_movies else [],
    })
