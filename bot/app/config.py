from pydantic_settings import BaseSettings
from typing import Optional

class BotSettings(BaseSettings):
    # Bot Configuration
    BOT_TOKEN: str = "8044942118:AAHaERN0mZSXJ-MHWFacl95qAXHfJdxW_Jk"
    BOT_WEBHOOK_URL: Optional[str] = None
    
    # Database
    BOT_DB_URL: str = "postgresql://daha_user:SWP2025@localhost/daha_db"
    BOT_SQLITE_URL: str = "sqlite+aiosqlite:///./bot.db"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8081
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Notification settings
    MAX_NOTIFICATION_LENGTH: int = 4096
    NOTIFICATION_RETRY_ATTEMPTS: int = 3
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = BotSettings() 