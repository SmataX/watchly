from contextlib import asynccontextmanager
from typing import Optional

import httpx
from pathlib import Path
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
BASE_DIR = Path(__file__).resolve().parent.parent
templates_dir = BASE_DIR / "templates"
static_dir = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
templates = Jinja2Templates(directory=str(templates_dir))

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
from src.routers.auth import router as router_auth
app.include_router(router_auth)



@app.get("/")
async def index(
    request: Request, 
    user: Optional[dict] = Depends(get_optional_user),
    client: httpx.AsyncClient = Depends(get_http_client)
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

    # Get 10 random movies from the api
    movies = []

    try:
        response = await client.get("/movies/random?limit=10")

        if response.status_code == 200:
            movies = response.json()
    except httpx.RequestError:
        pass

    return templates.TemplateResponse("index.html", {
        "request": request, 
        "user": user,
        "movies": movies
    })


@app.get("/all_movies")
async def movies(request: Request, client: httpx.AsyncClient = Depends(get_http_client)):
    movies = []
    try:
        response = await client.get(f"/movies/long")

        if response.status_code == 200:
            movies = response.json()
    except httpx.RequestError:
        pass



    return templates.TemplateResponse("all_movies.html", {
        "request": request, 
        "movies": movies
    })

@app.get("/profile/{username}")
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

@app.get("/friends")
def friends(request: Request, user: Optional[dict] = Depends(get_optional_user)):
    return templates.TemplateResponse("friends.html", {
        "request": request, 
        "user": user
    })

@app.get("/reviews")
def reviews(request: Request):
    return templates.TemplateResponse("reviews.html", {
        "request": request, 
    })
