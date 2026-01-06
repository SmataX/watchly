import httpx
from fastapi import APIRouter, Request, Form, status, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from src.main import templates
from src.core.deps import get_http_client, get_optional_user

router = APIRouter()


@router.get("/login", response_class=HTMLResponse)
def get_login_page(
    request: Request
):
    """Renders the login HTML page."""

    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
async def login_user(
    request: Request, 
    username: str = Form(...), 
    password: str = Form(...),
    client: httpx.AsyncClient = Depends(get_http_client)
):
    """Handles user login form submission."""

    try:
        response = await client.post(
            "/auth/login", 
            data={"username": username, "password": password}
        )
        response.raise_for_status()
        
        token_data = response.json()
        access_token = token_data.get("access_token")
        token_type = token_data.get("token_type")

        # Redirect to home page
        redirect_resp = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        
        # Securely set the cookie
        redirect_resp.set_cookie(
            key="access_token", 
            value=f"{token_type} {access_token}",
            httponly=True,
            max_age=1800,
            samesite="lax"
        )
        return redirect_resp

    except httpx.HTTPStatusError:
        return templates.TemplateResponse(
            "login.html", 
            {"request": request, "error": "Invalid Credentials"}
        )
    except httpx.RequestError as e:
        return templates.TemplateResponse(
            "login.html", 
            {"request": request, "error": "Backend service unavailable"}
        )
    

@router.get("/register", )
def get_register_page(request: Request):
    """Renders the register HTML page."""

    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
async def register_user(
    request: Request, 
    client: httpx.AsyncClient = Depends(get_http_client),
    username: str = Form(...), 
    email: str = Form(...),
    password: str = Form(...),
):
    """Handles user register"""

    try:
        response = await client.post(
            "/auth/register", 
            json={
                "username": username, 
                "email": email, 
                "password": password
            }
        )
        response.raise_for_status()
        
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    except httpx.HTTPStatusError:
        return templates.TemplateResponse(
            "register.html", 
            {"request": request, "error": "Registration failed"}
        )
    except httpx.RequestError as e:
        return templates.TemplateResponse(
            "register.html", 
            {"request": request, "error": "Backend service unavailable"}
        )


@router.get("/logout")
def logout():
    """Logs the user out."""

    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="access_token")
    return response
