from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
import logging
from app.models.url_model import URL
from app.schemas.url_schema import URLCreate
from app.utils.helpers import generate_short_code, validate_custom_code
from app.services.redis_service import redis_service
from app.config import settings

logger = logging.getLogger(__name__)

class URLService:
    def __init__(self, db: Session):
        self.db = db
    
    async def create_short_url(self, url_data: URLCreate) -> URL:
        """Create a new short URL"""
        original_url = str(url_data.original_url)
        
        # Check if URL already exists and is active
        existing_url = self.db.query(URL).filter(
            URL.original_url == original_url,
            URL.is_active == True
        ).first()
        
        if existing_url:
            logger.info(f"URL already exists: {existing_url.short_code}")
            return existing_url
        
        # Handle custom code
        if url_data.custom_code:
            if not validate_custom_code(
                url_data.custom_code, 
                settings.min_custom_code_length, 
                settings.max_custom_code_length
            ):
                raise ValueError("Invalid custom code format")
            
            # Check if custom code already exists
            if self.db.query(URL).filter(URL.short_code == url_data.custom_code).first():
                raise ValueError("Custom code already exists")
            
            short_code = url_data.custom_code
        else:
            # Generate unique short code
            short_code = self._generate_unique_short_code()
        
        # Create new URL entry
        db_url = URL(
            original_url=original_url,
            short_code=short_code
        )
        
        self.db.add(db_url)
        self.db.commit()
        self.db.refresh(db_url)
        
        # Cache the mapping
        await self._cache_url_data(db_url)
        
        logger.info(f"Created short URL: {short_code} -> {original_url}")
        return db_url
    
    async def get_original_url(self, short_code: str) -> Optional[str]:
        """Get original URL by short code and increment click count"""
        # Try cache first
        cached_data = await redis_service.get(f"url:{short_code}")
        if cached_data and cached_data.get("is_active"):
            # Increment click count
            await self._increment_click_count(short_code)
            return cached_data["original_url"]
        
        # Fallback to database
        db_url = self.db.query(URL).filter(
            URL.short_code == short_code,
            URL.is_active == True
        ).first()
        
        if not db_url:
            return None
        
        # Update cache
        await self._cache_url_data(db_url)
        
        # Increment click count
        await self._increment_click_count(short_code)
        
        return db_url.original_url
    
    def get_url_stats(self, short_code: str) -> Optional[URL]:
        """Get URL statistics"""
        return self.db.query(URL).filter(URL.short_code == short_code).first()
    
    def deactivate_url(self, short_code: str) -> bool:
        """Deactivate a URL"""
        db_url = self.db.query(URL).filter(URL.short_code == short_code).first()
        if db_url:
            db_url.is_active = False
            self.db.commit()
            # Remove from cache
            redis_service.delete(f"url:{short_code}")
            logger.info(f"Deactivated URL: {short_code}")
            return True
        return False
    
    def _generate_unique_short_code(self) -> str:
        """Generate a unique short code"""
        max_attempts = 10
        for _ in range(max_attempts):
            short_code = generate_short_code(settings.default_short_code_length)
            if not self.db.query(URL).filter(URL.short_code == short_code).first():
                return short_code
        
        # If we can't find a unique code, increase length
        return generate_short_code(settings.default_short_code_length + 2)
    
    async def _cache_url_data(self, url: URL):
        """Cache URL data in Redis"""
        await redis_service.set(
            f"url:{url.short_code}",
            {
                "original_url": url.original_url,
                "click_count": url.click_count,
                "is_active": url.is_active
            }
        )
    
    async def _increment_click_count(self, short_code: str):
        """Increment click count both in cache and database"""
        # Increment in database
        self.db.query(URL).filter(URL.short_code == short_code).update(
            {URL.click_count: URL.click_count + 1}
        )
        self.db.commit()
        
        # Increment in cache counter
        await redis_service.increment(f"clicks:{short_code}")
