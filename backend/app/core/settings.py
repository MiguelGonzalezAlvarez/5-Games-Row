import os
from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: str = "5 Games in a Row API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./5gamesrow.db")
    
    # Supabase (optional)
    SUPABASE_URL: Optional[str] = os.getenv("SUPABASE_URL")
    SUPABASE_KEY: Optional[str] = os.getenv("SUPABASE_KEY")
    SUPABASE_JWT_SECRET: Optional[str] = os.getenv("SUPABASE_JWT_SECRET")
    
    # Football API
    FOOTBALL_API_KEY: str = os.getenv("FOOTBALL_API_KEY", "")
    FOOTBALL_API_BASE_URL: str = "https://api.football-data.org/v4"
    
    # Redis (optional)
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:4321", 
        "http://localhost:3000",
        "https://5gamesrow.com"
    ]
    
    # Challenge
    HAIRCUT_CHALLENGE_START_DATE: str = "2024-10-05"
    MANCHESTER_UNITED_TEAM_ID: int = 66
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

# Alias for backwards compatibility
from .config import settings
