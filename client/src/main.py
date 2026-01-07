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
    movies = await get_data("/movies/random?limit=10", client)

    return templates.TemplateResponse("index.html", {
        "request": request, 
        "user": user,
        "movies": movies
    })