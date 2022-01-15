from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):

    DATABASE_HOSTNAME: str
    DATABASE_PORT: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_CREATE_TABLES: int

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
