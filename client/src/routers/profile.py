import httpx
from typing import Optional
from fastapi import APIRouter, Request, Form, status, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from src.main import templates
from src.core.deps import get_optional_user, get_http_client

router = APIRouter()

@router.get("/profile/{username}")
async def user_profile(
    request: Request, 
    user: Optional[dict] = Depends(get_optional_user),
    client: httpx.AsyncClient = Depends(get_http_client),
    username: str = ""
):
    user_data = None

    try:
        response = await client.get(f"/user/{username}")

        if response.status_code == 200:
            user_data = response.json()
    except httpx.RequestError:
        pass

    return templates.TemplateResponse("user_profile.html", {
        "request": request, 
        "user": user,
        "user_data": user_data,
    })