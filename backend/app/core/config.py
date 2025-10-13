from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App settings
    env: str = "development"
    log_level: str = "INFO"
    secret_key: str = "change_me"  # In production, use strong random key

    # Database
    database_url: str = "postgresql+asyncpg://user:pass@localhost/db"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # JWT
    jwt_secret_key: str = "change_me_jwt_secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
