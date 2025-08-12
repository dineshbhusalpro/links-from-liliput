import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "postgresql://username:password@localhost:5432/url_shortener_db")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/1")
    service_port: int = int(os.getenv("SERVICE_PORT", "8002"))
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    # Analytics settings
    cache_ttl: int = 300  # 5 minutes for analytics cache
    batch_size: int = 1000  # Batch size for processing
    
    class Config:
        env_file = ".env"

settings = Settings()