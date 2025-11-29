from contextlib import asynccontextmanager
from typing import Optional

import httpx
from fastapi import FastAPI, Request, Form, status, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from src.settings import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for the FastAPI app.
    
    Initializes a shared HTTP client on startup and closes it on shutdown.
    This improves performance by allowing connection pooling (keep-alive)
    to the backend API.
    """
    # Initialize the client with the base URL so we don't repeat it
    app.state.http_client = httpx.AsyncClient(base_url=settings.BACKEND_URL)
    yield
    # Clean up resources on shutdown
    await app.state.http_client.aclose()

app = FastAPI(lifespan=lifespan)

# --- Static Files & Templates ---
app.mount("/client/static", StaticFiles(directory="client/static"), name="static")
templates = Jinja2Templates(directory="client/templates")

# --- Dependencies ---

async def get_http_client(request: Request) -> httpx.AsyncClient:
    """
    Dependency to retrieve the shared HTTP client from app state.
    """
    return request.app.state.http_client

async def get_optional_user(
    request: Request, 
    client: httpx.AsyncClient = Depends(get_http_client)
) -> Optional[dict]:
    """
    Dependency that attempts to fetch the current user based on cookies.
    
    Args:
        request: The incoming HTTP request containing cookies.
        client: The shared HTTPX client.

    Returns:
        dict: The user data if the token is valid.
        None: If no token exists or the backend rejects the token.
    """
    token = request.cookies.get("access_token")
    if not token:
        return None

    try:
        response = await client.get(
            "/auth/get-user", 
            headers={"Authorization": token}
        )
        if response.status_code == 200:
            return response.json()
    except httpx.RequestError:
        # Log error here in a real app
        pass
        
    return None

# --- Routes ---

@app.get("/login", response_class=HTMLResponse)
def get_login_page(request: Request):
    """
    Renders the login HTML page.

    Args:
        request: The incoming HTTP request.

    Returns:
        TemplateResponse: The rendered 'login.html' template.
    """
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login_user(
    request: Request, 
    username: str = Form(...), 
    password: str = Form(...),
    client: httpx.AsyncClient = Depends(get_http_client)
):
    """
    Handles user login form submission.

    Authenticates against the backend API, retrieves a JWT token,
    and sets it as an HTTP-only cookie before redirecting.

    Args:
        request: The incoming HTTP request.
        username: Form data username.
        password: Form data password.
        client: Shared HTTP client dependency.

    Returns:
        RedirectResponse: Redirects to home on success.
        TemplateResponse: Re-renders login page on failure.
    """
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
    

@app.get("/register", )
def get_register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register_user(
    request: Request, 
    username: str = Form(...), 
    email: str = Form(...),
    password: str = Form(...),
    client: httpx.AsyncClient = Depends(get_http_client)
):
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

@app.get("/")
async def index(
    request: Request, 
    user: Optional[dict] = Depends(get_optional_user)
):
    """
    Renders the home page.

    Args:
        request: The incoming HTTP request.
        user: The user dictionary injected by the get_optional_user dependency.
              Will be None if the user is not logged in.

    Returns:
        TemplateResponse: The rendered 'template.html' with user context.
    """
    return templates.TemplateResponse("template.html", {
        "request": request, 
        "user": user
    })

@app.get("/logout")
def logout():
    """
    Logs the user out.

    Clears the access_token cookie and redirects the user back
    to the homepage (or login page).

    Returns:
        RedirectResponse: A redirect to the root path.
    """
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="access_token")
    return response