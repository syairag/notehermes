from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://notehermes:dev_password@localhost:5432/notehermes"
    REDIS_URL: str = "redis://localhost:6379"
    LLM_API_KEY: str = ""
    LLM_PROVIDER: str = "openrouter"
    AI_SERVICE_URL: str = "http://localhost:8001"
    JWT_SECRET: str = "dev-secret-change-in-prod"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173", "http://192.168.5.11:3000", "http://192.168.5.11:8000"]
    
    # Microsoft 365 Configuration (Century Internet / 21Vianet for China)
    USE_CHINA_M365: bool = False  # Set to True to use partner.outlook.cn
    M365_TENANT_ID: str = ""
    M365_CLIENT_ID: str = ""
    M365_CLIENT_SECRET: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
