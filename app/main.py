from fastapi import FastAPI

from app.config import settings
from app.lifespan import lifespan
from app.api.router import api_router
from app.middleware.auth import AuthMiddleware


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        lifespan=lifespan,
    )

    app.add_middleware(AuthMiddleware)

    app.include_router(api_router, prefix="/api")

    return app


app = create_app()
