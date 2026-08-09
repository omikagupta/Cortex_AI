from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ==========================
    # Application
    # ==========================
    APP_NAME: str = "AI Workspace Agent"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = Field(default="development")

    DEBUG: bool = True

    # ==========================
    # API
    # ==========================
    API_V1_PREFIX: str = "/api/v1"

    # ==========================
    # Database
    # ==========================
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str

    # ==========================
    # JWT
    # ==========================
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ==========================
    # Redis
    # ==========================
    REDIS_HOST: str
    REDIS_PORT: int

    # ==========================
    # AI
    # ==========================
    OLLAMA_BASE_URL: str
    EMBEDDING_MODEL: str
    LLM_MODEL: str
    GEMINI_API_KEY: str

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_DB}"
        )

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()