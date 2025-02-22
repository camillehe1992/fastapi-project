import os
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

if os.getenv("ENVIRONMENT", "local") == "local":
    load_dotenv()


class Settings(BaseSettings):
    """
    Application settings.
    """

    # FastAPI
    # Debug should be set to False on production
    DEBUG: Optional[bool] = os.getenv("DEBUG", "True") == "True"
    # Environment
    ENVIRONMENT: Optional[str] = os.getenv("ENVIRONMENT", "local")
    # Title is the name of application
    TITLE: Optional[str] = os.getenv("TITLE", "RestAPI")
    # Project version
    VERSION: Optional[str] = os.getenv("VERSION", "1.0.0")
    # Project nickname
    NICKNAME: Optional[str] = os.getenv("NICKNAME", "fastapi")
    #
    # SQLITE connection string
    SQLITE_CONNECTION_STRING: Optional[str] = os.getenv(
        "SQLITE_CONNECTION_STRING", "sqlite:///sqlite.db"
    )
    # JWT
    SECRET_KEY: Optional[str] = os.getenv("SECRET_KEY")
    ALGORITHM: Optional[str] = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: Optional[int] = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
    )
    # Origins
    ORIGINS: Optional[str] = os.getenv("ORIGINS", "")
    # PostgreSQL connection string
    POSTGRES_HOST: Optional[str] = os.getenv("POSTGRES_HOST", "127.0.0.1")
    POSTGRES_DB: Optional[str] = os.getenv("POSTGRES_DB")
    POSTGRES_USER: Optional[str] = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: Optional[str] = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_CONNECTION_STRING: str = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
    )


settings = Settings()
