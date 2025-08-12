import httpx
import logging
from typing import Dict, Any, Optional
from app.config import settings

logger = logging.getLogger(__name__)

class ServiceDiscovery:
    def __init__(self):
        self.services = {
            "url-service": settings.url_service_url
        }
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def forward_request(
        self, 
        service_name: str, 
        path: str, 
        method: str = "GET",
        **kwargs
    ) -> httpx.Response:
        """Forward request to appropriate microservice"""
        service_url = self.services.get(service_name)
        if not service_url:
            raise ValueError(f"Service {service_name} not found")
        
        url = f"{service_url}{path}"
        
        try:
            response = await self.client.request(method, url, **kwargs)
            return response
        except httpx.RequestError as e:
            logger.error(f"Request error to {service_name}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error forwarding to {service_name}: {e}")
            raise
    
    async def health_check(self, service_name: str) -> bool:
        """Check if service is healthy"""
        try:
            response = await self.forward_request(
                service_name, 
                "/health", 
                method="GET"
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed for {service_name}: {e}")
            return False