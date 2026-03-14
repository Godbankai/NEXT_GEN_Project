import sys
from contextlib import asynccontextmanager
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.app.core.config import settings
from backend.app.core.database import Base, engine
from backend.app.core.seed import ensure_default_admin
from backend.app.routers import admin, auth, exams, pages, proctor


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    ensure_default_admin()
    yield


app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="backend/app/static"), name="static")
app.mount("/storage", StaticFiles(directory=settings.media_root), name="storage")

app.include_router(pages.router)
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(exams.router, prefix="/api/exams", tags=["exams"])
app.include_router(proctor.router, prefix="/api/proctor", tags=["proctor"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
