from pydantic import BaseModel, HttpUrl, validator
from datetime import datetime
from typing import Optional

class URLCreate(BaseModel):
    original_url: HttpUrl
    custom_code: Optional[str] = None
    
    @validator('custom_code')
    def validate_custom_code(cls, v):
        if v is not None:
            if len(v) < 3 or len(v) > 20:
                raise ValueError('Custom code must be between 3 and 20 characters')
            if not all(c.isalnum() or c in '-_' for c in v):
                raise ValueError('Custom code can only contain letters, numbers, hyphens, and underscores')
        return v

class URLResponse(BaseModel):
    id: int
    original_url: str
    short_code: str
    short_url: str
    click_count: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class URLStats(BaseModel):
    short_code: str
    original_url: str
    click_count: int
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True

class ErrorResponse(BaseModel):
    error: str
    message: str