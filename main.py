import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config.app_config import configure_logging, get_settings
from app.database.schema.db import init_db
from app.routing.app import register_routes

configure_logging()
logger = logging.getLogger(__name__)
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="2.0.0",
    debug=settings.debug,
    description="Modular FastAPI backend for Student Management with auth, roles, and agent hooks.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event() -> None:
    logger.info("Starting application and initializing PostgreSQL schema")
    init_db()


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception):
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


register_routes(app)


@app.get("/")
def root():
    return {
        "message": "Student Management FastAPI is running",
        "docs": "/docs",
        "openapi": "/openapi.json",
        "health": "/api/v1/health",
    }
