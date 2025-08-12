from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.api.routes.analytics_routes import router
from app.database import engine
from app.models.analytics_model import Base
from app.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Analytics Service",
    description="Analytics and tracking service for URL shortener",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/analytics", tags=["analytics"])

@app.get("/health")
async def health_check():
    """Service health check"""
    return {"status": "healthy", "service": "analytics-service"}

@app.on_event("startup")
async def startup_event():
    logger.info("Analytics Service starting up...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Database URL: {settings.database_url}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Analytics Service shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.service_port)