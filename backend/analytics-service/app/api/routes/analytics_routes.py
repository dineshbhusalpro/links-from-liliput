from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Dict
import logging

from app.api.deps import get_db
from app.schemas.analytics_schema import ClickEventCreate, ClickEventResponse, AnalyticsStats
from app.services.analytics_service import AnalyticsService

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/events/", response_model=bool)
async def record_click_event(
    click_data: ClickEventCreate,
    db: Session = Depends(get_db)
):
    """Record a click event for analytics"""
    analytics_service = AnalyticsService(db)
    success = await analytics_service.record_click(click_data)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to record click event"
        )
    
    return success

@router.get("/stats/{short_code}", response_model=AnalyticsStats)
async def get_url_analytics(
    short_code: str,
    db: Session = Depends(get_db)
):
    """Get detailed analytics for a specific URL"""
    analytics_service = AnalyticsService(db)
    analytics = await analytics_service.get_analytics(short_code)
    
    if not analytics:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analytics not found for this URL"
        )
    
    return analytics

@router.get("/global", response_model=Dict)
async def get_global_analytics(db: Session = Depends(get_db)):
    """Get global analytics across all URLs"""
    analytics_service = AnalyticsService(db)
    return analytics_service.get_global_analytics()

@router.get("/health")
async def health_check():
    """Analytics service health check"""
    return {"status": "healthy", "service": "analytics-service"}