from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://notehermes:***@localhost:5432/notehermes"
    REDIS_URL: str = "redis://localhost:6379"
    LLM_API_KEY: str = ""
    LLM_PROVIDER: str = "openrouter"
    AI_SERVICE_URL: str = "http://localhost:8001"
    JWT_SECRET: str = "dev-secret-change-in-prod"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173", "http://192.168.5.11:3000", "http://192.168.5.11:8000"]
    
    # Microsoft 365 OAuth2 Configuration (世纪互联 / 21Vianet)
    # Get these from Azure AD app registration: https://portal.azure.cn
    M365_TENANT_ID: str = ""  # e.g. "your-tenant-id" or "common" for multi-tenant
    M365_CLIENT_ID: str = ""  # e.g. "your-client-id"
    M365_CLIENT_SECRET: str = ""  # e.g. "your-client-secret"

    class Config:
        env_file = ".env"

settings = Settings()
