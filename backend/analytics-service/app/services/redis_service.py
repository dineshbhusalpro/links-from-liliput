import redis
import json
import logging
from typing import Optional, Dict, Any
from app.config import settings

logger = logging.getLogger(__name__)

class RedisService:
    def __init__(self):
        try:
            self.client = redis.from_url(settings.redis_url, decode_responses=True)
            self.client.ping()
            logger.info("Analytics Redis connection established successfully")
        except Exception as e:
            logger.error(f"Analytics Redis connection failed: {e}")
            self.client = None
    
    def is_available(self) -> bool:
        return self.client is not None
    
    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        if not self.is_available():
            return None
            
        try:
            data = self.client.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            logger.error(f"Redis GET error for key {key}: {e}")
            return None
    
    async def set(self, key: str, value: Dict[str, Any], ttl: int = None) -> bool:
        if not self.is_available():
            return False
            
        try:
            ttl = ttl or settings.cache_ttl
            self.client.setex(key, ttl, json.dumps(value, default=str))
            return True
        except Exception as e:
            logger.error(f"Redis SET error for key {key}: {e}")
            return False

redis_service = RedisService()