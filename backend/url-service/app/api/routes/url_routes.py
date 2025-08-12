from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import List
import logging

from app.api.deps import get_db
from app.schemas.url_schema import URLCreate, URLResponse, URLStats, ErrorResponse
from app.services.url_service import URLService
from app.models.url_model import URL
from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/urls/", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
async def create_short_url(
    url_data: URLCreate,
    db: Session = Depends(get_db)
):
    """Create a new short URL"""
    try:
        url_service = URLService(db)
        db_url = await url_service.create_short_url(url_data)
        
        # Build response with full short URL
        return URLResponse(
            id=db_url.id,
            original_url=db_url.original_url,
            short_code=db_url.short_code,
            short_url=f"{settings.base_url}/{db_url.short_code}",
            click_count=db_url.click_count,
            is_active=db_url.is_active,
            created_at=db_url.created_at
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error creating short URL: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

@router.get("/urls/{short_code}/stats", response_model=URLStats)
async def get_url_stats(
    short_code: str,
    db: Session = Depends(get_db)
):
    """Get URL statistics"""
    url_service = URLService(db)
    db_url = url_service.get_url_stats(short_code)
    
    if not db_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found"
        )
    
    return URLStats(
        short_code=db_url.short_code,
        original_url=db_url.original_url,
        click_count=db_url.click_count,
        created_at=db_url.created_at,
        is_active=db_url.is_active
    )

@router.delete("/urls/{short_code}")
async def deactivate_url(
    short_code: str,
    db: Session = Depends(get_db)
):
    """Deactivate a URL"""
    url_service = URLService(db)
    success = url_service.deactivate_url(short_code)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL not found"
        )
    
    return {"message": "URL deactivated successfully"}

@router.get("/redirect/{short_code}")
async def redirect_to_original(
    short_code: str,
    db: Session = Depends(get_db)
):
    """Redirect to original URL"""
    url_service = URLService(db)
    original_url = await url_service.get_original_url(short_code)
    
    if not original_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Short URL not found or inactive"
        )
    
    return RedirectResponse(url=original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)

@router.get("/urls/", response_model=List[URLStats])
async def list_urls(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all URLs (for admin purposes)"""
    urls = db.query(URL).offset(skip).limit(limit).all()
    return [
        URLStats(
            short_code=url.short_code,
            original_url=url.original_url,
            click_count=url.click_count,
            created_at=url.created_at,
            is_active=url.is_active
        )
        for url in urls
    ]
