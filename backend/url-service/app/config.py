import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "postgresql://username:password@localhost:5432/url_shortener_db")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    service_port: int = int(os.getenv("SERVICE_PORT", "8001"))
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    # Redis cache settings
    cache_ttl: int = 3600  # 1 hour
    
    # URL shortening settings
    min_custom_code_length: int = 3
    max_custom_code_length: int = 20
    default_short_code_length: int = 6
    base_url: str = "http://localhost:8000"  # API Gateway URL

    class Config:
        env_file = ".env"

settings = Settings()