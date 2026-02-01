from fastapi import APIRouter

from app.api.health import router as health_router

# modules (we’ll add later)
# from app.modules.users.router import router as users_router

api_router = APIRouter()

api_router.include_router(health_router)
