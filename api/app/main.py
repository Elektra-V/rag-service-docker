# api/app/main.py
from fastapi import FastAPI
from pydantic_settings import BaseSettings
from qdrant_client import QdrantClient
import httpx

# Import routers after stdlib/third-party imports
from app.controllers.kb_controller import router as kb_router
from app.controllers.query_controller import router as query_router
from app.controllers.kb_controller import router as kb_router


# --- settings ---
class Settings(BaseSettings):
    APP_NAME: str = "rag-api"
    APP_VERSION: str = "0.1.0"
    QDRANT_URL: str = "http://qdrant:6333"
    OLLAMA_URL: str = "http://ollama:11434"

    class Config:
        env_file = ".env"


settings = Settings()


# --- FastAPI app ---
app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)


# --- health endpoints ---
@app.get("/health/live")
def live():
    return {"status": "alive"}


@app.get("/health/ready")
def ready():
    QdrantClient(url=settings.QDRANT_URL).get_collections()
    httpx.get(f"{settings.OLLAMA_URL}/api/tags", timeout=5).raise_for_status()
    return {"status": "ready"}


@app.get("/versions")
def versions():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "qdrant": settings.QDRANT_URL,
        "ollama": settings.OLLAMA_URL,
    }


# --- include routers ---
app.include_router(kb_router, prefix="/api/kb", tags=["kb"])
app.include_router(query_router, prefix="/api/query", tags=["query"])