from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_title: str = "Trading Data API"
    api_version: str = "1.0.0"
    api_description: str = "API for stock and cryptocurrency market data"
    
    # MCP Settings
    mcp_server_name: str = "trading-data-mcp"
    mcp_host: str = "0.0.0.0"
    mcp_port: int = 8001
    
    # CORS
    cors_origins: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
