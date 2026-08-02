from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers import cases, reports
from app.core.config import get_settings
from app.database.base import Base
from app.database.session import engine
import app.models  # noqa: F401

settings = get_settings()
app = FastAPI(title=settings.app_name, version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origin_list, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(cases.router, prefix="/api/v1")
app.include_router(reports.router, prefix="/api/v1")


@app.on_event("startup")
def create_database() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/api/v1/health", tags=["system"])
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}
