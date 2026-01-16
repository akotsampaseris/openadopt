"""
Application configuration.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "OpenAdopt"
    SECRET_KEY: str
    DEBUG: bool = False

    DATABASE_URL: str
    
    class Config:
        env_file = ".env"

settings = Settings()