from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os
from typing import ClassVar

class Settings(BaseSettings):
    app_name: str 
    database_url: str
    debug_mode: bool = False
    admin_email: str = "admin1@example.com"
    items_per_user: int = 150

    env_file_name: ClassVar[str] = ".env.development"
    # Dynamically set the env_file based on APP_ENV environment variable
    if os.getenv("APP_ENV") not in {"development", "testing", "production"}:
        env_file_name = ".env.development"
    else:
        env_file_name = ".env." + os.getenv("APP_ENV", "development")
    print(f"Loading environment variables from: {env_file_name}")
    
    
    model_config = SettingsConfigDict(
        env_file = env_file_name,
        env_file_encoding='utf-8',
        extra='ignore'  # Ignore extra fields in .env files
    )

    environment: str = Field("development", env="APP_ENV")
    database_url: str = Field("sqlite:///./dev.db", env="DATABASE_URL")
    api_key: str = Field("dev_api_key", env="API_KEY")
    debug_mode: bool = Field(True, env="DEBUG_MODE")
    app_name: str = Field("PB-FSSPTRG25", env="APP_NAME")

settings = Settings()