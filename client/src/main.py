from contextlib import asynccontextmanager
from typing import Optional

import httpx
from pathlib import Path
from fastapi import FastAPI, Request, Form, status, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from src.settings import settings
from src.core.deps import get_http_client, get_optional_user


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



# --- Routes ---
from src.routers.auth import router as router_auth
app.include_router(router_auth)

from src.routers.profile import router as router_profile
app.include_router(router_profile)



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


import asyncio

@app.get("/all_movies")
async def movies(request: Request, client: httpx.AsyncClient = Depends(get_http_client)):
    movies_list = []
    genres_list = []

    try:
        task_movies = client.get("/movies", params=request.query_params)
        task_genres = client.get("/movies/genres")

        results = await asyncio.gather(task_movies, task_genres, return_exceptions=True)
        
        res_movies, res_genres = results

        if not isinstance(res_movies, Exception) and res_movies.status_code == 200:
            movies_list = res_movies.json()
            
        if not isinstance(res_genres, Exception) and res_genres.status_code == 200:
            genres_list = res_genres.json()

    except Exception as e:
        print(f"Error fetching data: {e}")

    return templates.TemplateResponse("all_movies.html", {
        "request": request, 
        "movies": movies_list,
        "genres": genres_list
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

@app.get("/movie_page")
def movie_page(request: Request):
    return templates.TemplateResponse("movie_page.html", {
        "request": request, 
    })


@app.get("/movie/{movie_id}")
async def movie_detail(request: Request, movie_id: int, client: httpx.AsyncClient = Depends(get_http_client)):
    # 1. Pobieramy listę wszystkich filmów z Twojego serwera backendu (działa na porcie 8001)
    # Używamy tej samej ścieżki co w 'all_movies' (zakładam, że jest to /movies)
    try:
        response = await client.get("http://127.0.0.1:8001/movies")
        all_movies = response.json()
        
        # 2. Szukamy w tej liście filmu, który ma identyczne ID jak to w linku
        # Funkcja next() przeszukuje listę i zwraca pierwszy pasujący element
        selected_movie = next((m for m in all_movies if m["id"] == movie_id), None)
        
    except Exception as e:
        print(f"Błąd połączenia z backendem: {e}")
        selected_movie = None

    # 3. Zabezpieczenie: Jeśli filmu nie ma w bazie lub backend nie odpowiada
    if not selected_movie:
        selected_movie = {
            "title": "Nie znaleziono filmu",
            "overview": f"Nie udało się pobrać danych dla ID: {movie_id}",
            "poster_path": "", # Pusty plakat
            "genres": [],
            "global_rating": 0
        }

    # 4. Wysyłamy znaleziony film (selected_movie) do HTML jako zmienną "movie"
    return templates.TemplateResponse("movie_page.html", {
        "request": request, 
        "movie": selected_movie 
    })