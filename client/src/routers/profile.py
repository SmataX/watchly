from fastapi.responses import HTMLResponse
import httpx

from typing import Optional

from fastapi import APIRouter, Request, Depends, Form, status
from fastapi.responses import RedirectResponse

from src.main import templates
from src.core.deps import get_optional_user, get_http_client
from src.core.utils import get_data, send_data


router = APIRouter(prefix="/profile")


@router.get("/")
async def my_profile(
    request: Request, 
    user: Optional[dict] = Depends(get_optional_user),
    client: httpx.AsyncClient = Depends(get_http_client),
):
    if not user:
        return RedirectResponse("http://127.0.0.1:8001/login")
    
    user_data = await get_data(f"/user/{user['username']}", client)
    if user and "id" not in user_data:
        user_data["id"] = user.get("id")

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
    client: httpx.AsyncClient = Depends(get_http_client),
    user: Optional[dict] = Depends(get_optional_user)
):
    if not user:
        return RedirectResponse(url="/login") 

    user_data = await get_data(f"/user/{ user['username'] }", client)

    return templates.TemplateResponse("edit_profile.html", {
        "request": request,
        "user": user,
        "user_data": user_data,
    })

@router.post("/edit", response_class=RedirectResponse)
async def handle_edit_profile(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    description: Optional[str] = Form(None),
    client: httpx.AsyncClient = Depends(get_http_client),
    user: Optional[dict] = Depends(get_optional_user)
):
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    payload = {
        "user_id": user['id'],
        "username": username,
        "email": email,
        "description": description if description else ""
    }

    token = request.cookies.get("access_token")
    if token and "Bearer" in token:
        token = token.split(" ")[1]


    result = await send_data(
        url="http://127.0.0.1:8001/user/update",
        payload=payload,
        client=client,
        method="PATCH",
        token=token,
        as_form=True 
    )

    if result:
        return RedirectResponse(
            url=f"/logout", 
            status_code=status.HTTP_303_SEE_OTHER
        )

    return RedirectResponse(
        url="/profile/edit", 
        status_code=status.HTTP_303_SEE_OTHER
    )


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