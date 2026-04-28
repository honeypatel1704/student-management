from functools import lru_cache

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Student Management API"
    app_env: str = "development"
    debug: bool = True

    postgres_dsn: str = Field(
        default="postgresql+psycopg2://postgres:postgres@localhost:5432/student_db",
        validation_alias=AliasChoices("DATABASE_URL", "POSTGRES_DSN"),
    )

    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    bootstrap_admin_name: str = "System Admin"
    bootstrap_admin_email: str = "admin@student.com"
    bootstrap_admin_password: str = "Admin@123"

    log_level: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
