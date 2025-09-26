from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    app_env: str = "development"
    secret_key: str = "default-secret-key-change-in-production"
    telegram_bot_token: str = ""
    database_url: str = "postgresql+asyncpg://postgres:postgres@db:5432/postgres"
    supabase_url: str = ""
    supabase_key: str = ""
    initdata_max_age_seconds: int = 86400
    admin_token: str = ""
    cors_origins: str = "*"
    
    @property
    def cors_origins_list(self) -> List[str]:
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()