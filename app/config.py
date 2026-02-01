# import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "WMS Backend"
    DEBUG: bool = False
    API_PREFIX: str = "/api"

    DATABASE_URL: str
    REDIS_URL: str

    SECRET_KEY: str
    SESSION_TTL_SECONDS: int = 60 * 60 * 24 * 7
    COOKIE_NAME: str = "wms_session"
    COOKIE_SECURE: bool = False  #we will set it to True in production
    COOKIE_HTTPONLY: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
