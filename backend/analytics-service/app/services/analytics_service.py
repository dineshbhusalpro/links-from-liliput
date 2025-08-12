from sqlalchemy.orm import Session
from sqlalchemy import func, distinct, and_
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import json
import logging
from collections import Counter

from app.models.analytics_model import ClickEvent, AnalyticsReport as AnalyticsReportModel
from app.schemas.analytics_schema import (
    ClickEventCreate, AnalyticsStats, TopStats, 
    TimeSeriesData, AnalyticsReport
)
from app.services.redis_service import redis_service

logger = logging.getLogger(__name__)

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db
    
    async def record_click(self, click_data: ClickEventCreate) -> bool:
        """Record a click event"""
        try:
            click_event = ClickEvent(**click_data.dict())
            self.db.add(click_event)
            self.db.commit()
            
            # Invalidate cache for this short_code
            await redis_service.set(f"analytics:invalidate:{click_data.short_code}", {"timestamp": datetime.now().isoformat()})
            
            logger.info(f"Recorded click for {click_data.short_code} from {click_data.ip_address}")
            return True
        except Exception as e:
            logger.error(f"Error recording click: {e}")
            self.db.rollback()
            return False
    
    async def get_analytics(self, short_code: str) -> Optional[AnalyticsStats]:
        """Get comprehensive analytics for a short code"""
        # Try cache first
        cache_key = f"analytics:stats:{short_code}"
        cached_data = await redis_service.get(cache_key)
        if cached_data:
            return AnalyticsStats(**cached_data)
        
        try:
            # Calculate date ranges
            now = datetime.utcnow()
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            week_start = today_start - timedelta(days=7)
            month_start = today_start - timedelta(days=30)
            
            # Base query
            base_query = self.db.query(ClickEvent).filter(ClickEvent.short_code == short_code)
            
            # Total and unique clicks
            total_clicks = base_query.count()
            unique_clicks = base_query.with_entities(distinct(ClickEvent.ip_address)).count()
            
            # Time-based clicks
            clicks_today = base_query.filter(ClickEvent.timestamp >= today_start).count()
            clicks_this_week = base_query.filter(ClickEvent.timestamp >= week_start).count()
            clicks_this_month = base_query.filter(ClickEvent.timestamp >= month_start).count()
            
            # Top countries
            country_data = self.db.query(
                ClickEvent.country, 
                func.count(ClickEvent.id).label('count')
            ).filter(
                and_(ClickEvent.short_code == short_code, ClickEvent.country.isnot(None))
            ).group_by(ClickEvent.country).order_by(func.count(ClickEvent.id).desc()).limit(5).all()
            
            top_countries = [TopStats(name=country or "Unknown", count=count) for country, count in country_data]
            
            # Top referers
            referer_data = self.db.query(
                ClickEvent.referer, 
                func.count(ClickEvent.id).label('count')
            ).filter(
                and_(ClickEvent.short_code == short_code, ClickEvent.referer.isnot(None))
            ).group_by(ClickEvent.referer).order_by(func.count(ClickEvent.id).desc()).limit(5).all()
            
            top_referers = [TopStats(name=referer or "Direct", count=count) for referer, count in referer_data]
            
            # Click timeline (last 30 days)
            timeline_data = self.db.query(
                func.date(ClickEvent.timestamp).label('date'),
                func.count(ClickEvent.id).label('clicks')
            ).filter(
                and_(ClickEvent.short_code == short_code, ClickEvent.timestamp >= month_start)
            ).group_by(func.date(ClickEvent.timestamp)).order_by(func.date(ClickEvent.timestamp)).all()
            
            click_timeline = [TimeSeriesData(date=str(date), clicks=clicks) for date, clicks in timeline_data]
            
            analytics = AnalyticsStats(
                short_code=short_code,
                total_clicks=total_clicks,
                unique_clicks=unique_clicks,
                clicks_today=clicks_today,
                clicks_this_week=clicks_this_week,
                clicks_this_month=clicks_this_month,
                top_countries=top_countries,
                top_referers=top_referers,
                click_timeline=click_timeline
            )
            
            # Cache the result
            await redis_service.set(cache_key, analytics.dict())
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting analytics for {short_code}: {e}")
            return None
    
    def get_global_analytics(self) -> Dict:
        """Get global analytics across all URLs"""
        try:
            now = datetime.utcnow()
            today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            week_start = today_start - timedelta(days=7)
            
            total_clicks = self.db.query(ClickEvent).count()
            unique_ips = self.db.query(distinct(ClickEvent.ip_address)).count()
            clicks_today = self.db.query(ClickEvent).filter(ClickEvent.timestamp >= today_start).count()
            clicks_this_week = self.db.query(ClickEvent).filter(ClickEvent.timestamp >= week_start).count()
            
            # Top URLs by clicks
            top_urls = self.db.query(
                ClickEvent.short_code,
                func.count(ClickEvent.id).label('clicks')
            ).group_by(ClickEvent.short_code).order_by(func.count(ClickEvent.id).desc()).limit(10).all()
            
            return {
                "total_clicks": total_clicks,
                "unique_visitors": unique_ips,
                "clicks_today": clicks_today,
                "clicks_this_week": clicks_this_week,
                "top_urls": [{"short_code": code, "clicks": clicks} for code, clicks in top_urls]
            }
        except Exception as e:
            logger.error(f"Error getting global analytics: {e}")
            return {}
