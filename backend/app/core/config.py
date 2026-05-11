from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    # App settings
    env: str = "development"
    log_level: str = "INFO"
    secret_key: str = Field(default="change_me", env="SECRET_KEY")  # In production, use strong random key

    # Database
    database_url: str = Field(default="postgresql+asyncpg://postgres:postgres@db:5432/migration_db", env="DATABASE_URL")

    # Redis
    redis_url: str = Field(default="redis://redis:6379/0", env="REDIS_URL")

    # JWT
    jwt_secret_key: str = Field(default="change_me_jwt_secret", env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=60, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"

# Global settings instance
settings = Settings()