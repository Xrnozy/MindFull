"""
Mindfull Application Configuration.

Uses Pydantic v2 BaseSettings for type-safe configuration management
with environment variable overrides and .env file support.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application-wide configuration."""

    # ──────────────────────────────────────────────
    # General
    # ──────────────────────────────────────────────
    PROJECT_NAME: str = "Mindfull API"
    PROJECT_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"  # development | staging | production
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"

    # ──────────────────────────────────────────────
    # PostgreSQL / Supabase
    # ──────────────────────────────────────────────
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "mindfull"
    POSTGRES_PASSWORD: str = "mindfull_password"
    POSTGRES_DB: str = "mindfull_db"
    POSTGRES_PORT: str = "5432"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_ECHO: bool = False

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def DATABASE_URL_SYNC(self) -> str:
        """Synchronous URL for Alembic migrations."""
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # ──────────────────────────────────────────────
    # Redis
    # ──────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_DB: int = 1
    REDIS_DEFAULT_TTL: int = 300  # 5 minutes

    # ──────────────────────────────────────────────
    # Supabase
    # ──────────────────────────────────────────────
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SUPABASE_JWT_SECRET: str = ""
    SUPABASE_SERVICE_ROLE_KEY: str = ""

    # ──────────────────────────────────────────────
    # JWT / Auth
    # ──────────────────────────────────────────────
    JWT_SECRET_KEY: str = "CHANGE-ME-IN-PRODUCTION"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    API_KEY_PREFIX: str = "mf_live_"

    # ──────────────────────────────────────────────
    # CORS
    # ──────────────────────────────────────────────
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://*.vercel.app",
    ]

    # ──────────────────────────────────────────────
    # Rate Limiting
    # ──────────────────────────────────────────────
    RATE_LIMIT_DEFAULT_PER_MINUTE: int = 60
    RATE_LIMIT_AUTH_PER_MINUTE: int = 10
    RATE_LIMIT_ANALYTICS_PER_MINUTE: int = 120

    # ──────────────────────────────────────────────
    # Celery
    # ──────────────────────────────────────────────
    CELERY_BROKER_URL: str = "redis://localhost:6379/2"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/3"

    # ──────────────────────────────────────────────
    # Monitoring
    # ──────────────────────────────────────────────
    ENABLE_METRICS: bool = True
    ENABLE_TRACING: bool = False
    OTEL_EXPORTER_OTLP_ENDPOINT: str = "http://localhost:4317"
    LOG_LEVEL: str = "INFO"

    # ──────────────────────────────────────────────
    # Sustainability Engine
    # ──────────────────────────────────────────────
    DEFAULT_PUE: float = 1.1  # Power Usage Effectiveness
    DEFAULT_CARBON_INTENSITY_G_PER_KWH: float = 429.0  # US average grid

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        env_file_encoding="utf-8",
    )


settings = Settings()
