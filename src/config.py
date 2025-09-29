from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DEFAULT_DB_NAME: str
    DEBUG: bool

    DATABASE_URL: str | None = None
    DEFAULT_DATABASE_URL: str | None = None

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_EXPIRE_IN: int

    class Config:
        env_file = BASE_DIR / ".env"
        env_file_encoding = "utf-8"


    @property
    def db_url(self) -> str:
        return (self.DATABASE_URL or
                f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")

    @property
    def default_db_url(self) -> str:
        return (self.DEFAULT_DATABASE_URL or
                f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DEFAULT_DB_NAME}")


settings = Settings()
