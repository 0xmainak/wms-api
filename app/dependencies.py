from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.infrastructure.db.session import SessionLocal
from app.infrastructure.cache.redis import redis_client
from fastapi import HTTPException, Request


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


def get_current_user(request: Request):
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(401, "Not authenticated")

    return user

def require_user(request: Request):
    user = getattr(request.state, "user", None)

    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return user