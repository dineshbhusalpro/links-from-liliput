from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.sql import func
from app.database import Base

class ClickEvent(Base):
    __tablename__ = "click_events"
    
    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String(50), nullable=False, index=True)
    user_agent = Column(Text)
    ip_address = Column(String(45), index=True)  # Support IPv6
    referer = Column(Text)
    country = Column(String(2))  # ISO country code
    city = Column(String(100))
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    def __repr__(self):
        return f"<ClickEvent(short_code='{self.short_code}', ip='{self.ip_address}')>"

class AnalyticsReport(Base):
    __tablename__ = "analytics_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String(50), nullable=False, index=True)
    report_type = Column(String(50), nullable=False)  # daily, weekly, monthly
    report_date = Column(DateTime(timezone=True), nullable=False, index=True)
    total_clicks = Column(Integer, default=0)
    unique_clicks = Column(Integer, default=0)
    top_countries = Column(Text)  # JSON string
    top_referers = Column(Text)   # JSON string
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<AnalyticsReport(short_code='{self.short_code}', type='{self.report_type}')>"
