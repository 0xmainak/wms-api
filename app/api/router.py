from fastapi import APIRouter

from app.api.health import router as health_router

from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.roles.router import router as roles_router


api_router = APIRouter()

#system routes
api_router.include_router(health_router)

#module routes
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(roles_router)
