from fastapi import HTTPException
from sqlalchemy.orm import Session
import redis

from app.core.security import verify_password, generate_session_id
from app.config import settings
from .repository import AuthRepository


class AuthService:
    def __init__(self, db: Session, redis_client: redis.Redis):
        self.repo = AuthRepository(db)
        self.redis = redis_client

    def login(self, email: str, password: str) -> tuple[str, int]:
        user = self.repo.get_by_email(email)

        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(401, "Invalid credentials")

        if not user.is_active:
            raise HTTPException(403, "User disabled")

        session_id = generate_session_id()

        self.redis.setex(
            f"session:{session_id}",
            settings.SESSION_TTL_SECONDS,
            user.id,
        )

        return session_id, user.id

    def logout(self, session_id: str):
        self.redis.delete(f"session:{session_id}")

    def get_user_from_session(self, session_id: str):
        user_id = self.redis.get(f"session:{session_id}")
        if not user_id:
            return None

        return self.repo.get_by_id(int(user_id))

    def refresh(self, session_id: str):
        self.redis.expire(f"session:{session_id}", settings.SESSION_TTL_SECONDS)
