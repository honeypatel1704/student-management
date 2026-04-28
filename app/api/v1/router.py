from fastapi import APIRouter

from app.api.v1.endpoints import agents, attendance, auth, health, students

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(students.router)
api_router.include_router(attendance.router)
api_router.include_router(agents.router)
