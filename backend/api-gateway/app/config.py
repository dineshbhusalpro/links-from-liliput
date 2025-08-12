import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    url_service_url: str = os.getenv("URL_SERVICE_URL", "http://localhost:8001")
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    api_key: str = os.getenv("API_KEY", "default-gateway-key")
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    class Config:
        env_file = ".env"

settings = Settings()