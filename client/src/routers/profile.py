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
        return RedirectResponse("/login")
    
    user_data = await get_data(f"/user/{user['username']}", client)

    return templates.TemplateResponse("profile.html", {
        "request": request, 
        "user": user,
        "user_data": user_data,
    })


@router.get("/{username}")
async def user_profile(
    request: Request, 
    user: Optional[dict] = Depends(get_optional_user),
    client: httpx.AsyncClient = Depends(get_http_client),
    username: str = ""
):
    user_data = await get_data(f"/user/{username}", client)

    return templates.TemplateResponse("profile.html", {
        "request": request, 
        "user": user,
        "user_data": user_data,
    })