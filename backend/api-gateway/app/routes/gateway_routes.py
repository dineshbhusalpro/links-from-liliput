from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import JSONResponse, RedirectResponse
import httpx
import logging
from app.services.service_discovery import ServiceDiscovery
from app.middleware.rate_limiter import RateLimiter
from app.middleware.auth_middleware import AuthMiddleware
from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize services
service_discovery = ServiceDiscovery()
rate_limiter = RateLimiter(settings.redis_url, settings.rate_limit_per_minute)
auth_middleware = AuthMiddleware(settings.api_key)

@router.get("/health")
async def gateway_health():
    """Gateway health check"""
    return {"status": "healthy", "service": "api-gateway"}

@router.get("/health/all")
async def all_services_health():
    """Check health of all services"""
    services_health = {}
    
    for service_name in ["url-service"]:
        services_health[service_name] = await service_discovery.health_check(service_name)
    
    all_healthy = all(services_health.values())
    status_code = 200 if all_healthy else 503
    
    return JSONResponse(
        status_code=status_code,
        content={
            "gateway": "healthy",
            "services": services_health,
            "overall_status": "healthy" if all_healthy else "unhealthy"
        }
    )

# URL Service Routes
@router.post("/api/v1/shorten")
async def create_short_url(request: Request):
    """Create short URL - forwarded to URL service"""
    await rate_limiter.check_rate_limit(request)
    
    try:
        body = await request.json()
        response = await service_discovery.forward_request(
            "url-service",
            "/urls/",
            method="POST",
            json=body,
            headers={"Content-Type": "application/json"}
        )
        
        return JSONResponse(
            status_code=response.status_code,
            content=response.json()
        )
    except httpx.RequestError as e:
        logger.error(f"Failed to forward request: {e}")
        raise HTTPException(status_code=503, detail="URL service unavailable")
    except Exception as e:
        logger.error(f"Error creating short URL: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/api/v1/urls/{short_code}/stats")
async def get_url_stats(short_code: str, request: Request):
    """Get URL statistics - forwarded to URL service"""
    await rate_limiter.check_rate_limit(request)
    
    try:
        response = await service_discovery.forward_request(
            "url-service",
            f"/urls/{short_code}/stats",
            method="GET"
        )
        
        return JSONResponse(
            status_code=response.status_code,
            content=response.json()
        )
    except httpx.RequestError as e:
        logger.error(f"Failed to forward request: {e}")
        raise HTTPException(status_code=503, detail="URL service unavailable")
    except Exception as e:
        logger.error(f"Error getting URL stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/api/v1/urls/{short_code}")
async def deactivate_url(
    short_code: str, 
    request: Request,
    authenticated: bool = Depends(auth_middleware.verify_api_key)
):
    """Deactivate URL - requires authentication"""
    await rate_limiter.check_rate_limit(request)
    
    try:
        response = await service_discovery.forward_request(
            "url-service",
            f"/urls/{short_code}",
            method="DELETE"
        )
        
        return JSONResponse(
            status_code=response.status_code,
            content=response.json()
        )
    except httpx.RequestError as e:
        logger.error(f"Failed to forward request: {e}")
        raise HTTPException(status_code=503, detail="URL service unavailable")
    except Exception as e:
        logger.error(f"Error deactivating URL: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/{short_code}")
async def redirect_to_original(short_code: str, request: Request):
    """Redirect to original URL"""
    await rate_limiter.check_rate_limit(request)
    
    try:
        response = await service_discovery.forward_request(
            "url-service",
            f"/redirect/{short_code}",
            method="GET"
        )
        
        if response.status_code == 307:
            # Extract redirect URL from response
            redirect_url = response.headers.get("location")
            if redirect_url:
                return RedirectResponse(url=redirect_url, status_code=307)
        
        return JSONResponse(
            status_code=response.status_code,
            content=response.json()
        )
    except httpx.RequestError as e:
        logger.error(f"Failed to forward request: {e}")
        raise HTTPException(status_code=503, detail="URL service unavailable")
    except Exception as e:
        logger.error(f"Error redirecting: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
