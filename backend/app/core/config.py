import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database settings
    database_url: str = "postgresql+asyncpg://daha_user:SWP2025@localhost/daha_db"
    database_pool_size: int = 20
    database_max_overflow: int = 30
    database_pool_pre_ping: bool = True
    database_pool_recycle: int = 3600
    
    # API settings
    api_title: str = "Daha Admin API"
    api_description: str = "API for managing courses, subjects, and educational resources"
    api_version: str = "1.0.0"
    debug: bool = True
    
    # CORS settings
    allowed_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173"
    ]
    
    # Logging settings
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Pagination settings
    default_page_size: int = 20
    max_page_size: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings() 