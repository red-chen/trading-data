from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_TITLE: str = "Trading Data API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "API for stock and cryptocurrency market data"
    
    # MCP Settings
    MCP_SERVER_NAME: str = "trading-data-mcp"
    MCP_HOST: str = "0.0.0.0"
    MCP_PORT: int = 8001
    
    # CORS
    CORS_ORIGINS: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignore extra fields from .env


settings = Settings()
