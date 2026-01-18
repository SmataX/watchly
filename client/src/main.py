import httpx

from contextlib import asynccontextmanager
from typing import Optional
from pathlib import Path

from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from src.settings import settings
from src.core.deps import get_http_client, get_optional_user
from src.core.utils import get_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(base_url=settings.BACKEND_URL)
    yield
    await app.state.http_client.aclose()

app = FastAPI(lifespan=lifespan)


# --- Static Files & Templates ---
BASE_DIR = Path(__file__).resolve().parent.parent
templates_dir = BASE_DIR / "templates"
static_dir = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
templates = Jinja2Templates(directory=str(templates_dir))


# --- Routers ---
from src.routers.auth import router as router_auth
app.include_router(router_auth)

from src.routers.profile import router as router_profile
app.include_router(router_profile)

from src.routers.movies import router as router_movies
app.include_router(router_movies)


# --- Routes ---
@app.get("/")
async def index(
    request: Request, 
    user: Optional[dict] = Depends(get_optional_user),
    client: httpx.AsyncClient = Depends(get_http_client)
):
    trending_movies = await get_data("/movies/trending?limit=8", client)
    movies = await get_data("/movies/random?limit=8", client)

    if len(trending_movies) < 8:
        trending_movies.extend(movies[:8-len(trending_movies)])

    return templates.TemplateResponse("index.html", {
        "request": request, 
        "user": user,
        "movies": movies,
        "trending": trending_movies, 
    })

@app.get("/api/search_movies")
async def search_combined_api(request: Request, query: str, client: httpx.AsyncClient = Depends(get_http_client)):
    if not query or len(query) < 3:
        return []
    
    results = []
    
    try:
        #1. Get movies
        response_movies = await client.get("/movies/search", params={"title": query, "limit": 5})
        
        movies = response_movies.json()
        print(movies)
        for m in movies:
            results.append({
                "id": m["id"],
                "title": m["title"],
                "type": "movie",
                "url": f"/movies/{m['id']}"
            })

        response_users = await client.get("/user/search", params={"username": query, "limit": 5})

        if response_users.status_code == 200:
            users = response_users.json()
            for u in users:
                results.append({
                    "title": u["username"],
                    "type": "user",
                    "url": f"/profile/{u['username']}"
                })
    except httpx.HTTPError:
        pass
    return results