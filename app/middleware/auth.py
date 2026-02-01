from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

from app.config import settings
from app.infrastructure.cache.redis import redis_client
from app.infrastructure.db.session import SessionLocal
from app.modules.auth.repository import AuthRepository


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        session_id = request.cookies.get(settings.COOKIE_NAME)

        if session_id:
            user_id = redis_client.get(f"session:{session_id}")
            if user_id:
                db = SessionLocal()
                repo = AuthRepository(db)
                user = repo.get_by_id(int(user_id))
                request.state.user = user
                db.close()

        response = await call_next(request)
        return response
