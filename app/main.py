from fastapi import FastAPI

from app.api.router import api_router
from app.config import settings

from app.modules.auth.router import router as auth_router
from app.middleware.auth import AuthMiddleware

from app.lifespan import lifespan

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        lifespan=lifespan
    )

    app.include_router(api_router, prefix="/api")

    return app


app = create_app()

app.add_middleware(AuthMiddleware)
app.include_router(auth_router, prefix="/api")
