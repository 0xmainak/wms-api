from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.infrastructure.db.session import SessionLocal
from app.infrastructure.cache.redis import redis_client


# DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Redis
def get_redis():
    return redis_client


# Placeholder (we’ll implement later)
def get_current_user(request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(401, "Not authenticated")
    return user
