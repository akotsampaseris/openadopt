"""
Application configuration.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_NAME: str = "OpenAdopt"
    SECRET_KEY: str
    DEBUG: bool = False

    # DB
    DATABASE_URL: str

    # Auth
    ACCESS_TOKEN_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # Pagination
    DEFAULT_PAGE_SIZE: int = 50
    MAX_PAGE_SIZE: int = 100

    # Storage
    STORAGE_BACKEND: str = "local"
    STORAGE_LOCAL_PATH: str
    STORAGE_LOCAL_URL: str

    class Config:
        env_file = "../.env"
        extra = "ignore"


settings = Settings()
