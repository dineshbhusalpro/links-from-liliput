from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Optional

class ClickEventCreate(BaseModel):
    short_code: str
    user_agent: Optional[str] = None
    ip_address: str
    referer: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None

class ClickEventResponse(BaseModel):
    id: int
    short_code: str
    user_agent: Optional[str]
    ip_address: str
    referer: Optional[str]
    country: Optional[str]
    city: Optional[str]
    timestamp: datetime
    
    class Config:
        from_attributes = True

class TopStats(BaseModel):
    name: str
    count: int

class TimeSeriesData(BaseModel):
    date: str
    clicks: int

class AnalyticsStats(BaseModel):
    short_code: str
    total_clicks: int
    unique_clicks: int
    clicks_today: int
    clicks_this_week: int
    clicks_this_month: int
    top_countries: List[TopStats]
    top_referers: List[TopStats]
    click_timeline: List[TimeSeriesData]

class AnalyticsReport(BaseModel):
    short_code: str
    report_type: str
    report_date: datetime
    total_clicks: int
    unique_clicks: int
    top_countries: List[TopStats]
    top_referers: List[TopStats]
    
    class Config:
        from_attributes = True