from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router


BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR / "frontend"


app = FastAPI(
    title="SmartDoc-RAG",
    description="Simple document-based RAG application",
    version="1.0.0",
)


app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static",
)


@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


app.include_router(router)