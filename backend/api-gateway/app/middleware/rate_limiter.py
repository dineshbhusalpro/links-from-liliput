import redis
import time
from fastapi import HTTPException, Request
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class RateLimiter:
    def __init__(self, redis_url: str, requests_per_minute: int = 60):
        try:
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            self.requests_per_minute = requests_per_minute
            self.window_size = 60  # 60 seconds
        except Exception as e:
            logger.error(f"Failed to connect to Redis for rate limiting: {e}")
            self.redis_client = None
    
    async def check_rate_limit(self, request: Request) -> bool:
        """Check if request is within rate limit"""
        if not self.redis_client:
            return True  # Allow if Redis is not available
        
        client_ip = request.client.host
        current_time = int(time.time())
        window_start = current_time - self.window_size
        
        # Create a unique key for this IP
        key = f"rate_limit:{client_ip}"
        
        try:
            # Remove old entries
            self.redis_client.zremrangebyscore(key, 0, window_start)
            
            # Count current requests
            current_requests = self.redis_client.zcard(key)
            
            if current_requests >= self.requests_per_minute:
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded. Please try again later."
                )
            
            # Add current request
            self.redis_client.zadd(key, {str(current_time): current_time})
            self.redis_client.expire(key, self.window_size)
            
            return True
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Rate limiting error: {e}")
            return True  # Allow if there's an error