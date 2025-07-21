from pydantic_settings import BaseSettings
from pydantic import model_validator
from typing import List
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://daha_user:SWP2025@localhost/daha_db"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 30
    DATABASE_POOL_PRE_PING: bool = True
    DATABASE_POOL_RECYCLE: int = 3600
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] | str = ["http://localhost:3000", "http://localhost:5173"]
    
    @model_validator(mode='before')
    def assemble_allowed_origins(cls, values):
        allowed_origins = values.get('ALLOWED_ORIGINS')
        if isinstance(allowed_origins, str):
            values['ALLOWED_ORIGINS'] = [i.strip() for i in allowed_origins.split(',')]
        return values

    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Daha"
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Redis cache settings
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Rate limiting settings
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_TIMESCALE: int = 60  # in seconds
    
    # Bot settings
    BOT_API_KEY: str = "your_secret_bot_api_key"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
