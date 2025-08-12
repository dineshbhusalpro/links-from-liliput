from fastapi import HTTPException, Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import logging

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)

class AuthMiddleware:
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    async def verify_api_key(
        self, 
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
    ) -> bool:
        """Verify API key for protected endpoints"""
        if not credentials:
            raise HTTPException(
                status_code=401,
                detail="Authentication required"
            )
        
        if credentials.credentials != self.api_key:
            raise HTTPException(
                status_code=401,
                detail="Invalid API key"
            )
        
        return True