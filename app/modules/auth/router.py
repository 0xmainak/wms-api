from fastapi import APIRouter, Depends, Response, Request, HTTPException

from app.dependencies import get_db, get_redis
from app.config import settings

from .schemas import LoginRequest, UserResponse
from .service import AuthService


router = APIRouter(prefix="/auth", tags=["Auth"])


def get_service(db=Depends(get_db), redis_client=Depends(get_redis)):
    return AuthService(db, redis_client)


@router.post("/login")
def login(data: LoginRequest, response: Response, service: AuthService = Depends(get_service)):
    session_id, _ = service.login(data.email, data.password)

    response.set_cookie(
        key=settings.COOKIE_NAME,
        value=session_id,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        max_age=settings.SESSION_TTL_SECONDS,
    )

    return {"message": "logged in"}


@router.post("/logout")
def logout(request: Request, response: Response, service: AuthService = Depends(get_service)):
    session_id = request.cookies.get(settings.COOKIE_NAME)

    if session_id:
        service.logout(session_id)

    response.delete_cookie(settings.COOKIE_NAME)

    return {"message": "logged out"}


@router.get("/me", response_model=UserResponse)
def me(request: Request):
    user = getattr(request.state, "user", None)

    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    return user

@router.post("/refresh")
def refresh(request: Request, service: AuthService = Depends(get_service)):
    session_id = request.cookies.get(settings.COOKIE_NAME)

    if not session_id:
        raise HTTPException(401, "Not authenticated")

    service.refresh(session_id)

    return {"message": "refreshed"}

