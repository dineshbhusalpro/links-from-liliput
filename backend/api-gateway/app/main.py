from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.routes.gateway_routes import router
from app.middleware.logging_middleware import LoggingMiddleware
from app.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="URL Shortener API Gateway",
    description="API Gateway for URL Shortener Microservices",
    version="1.0.0",
)

# Add middleware
app.add_middleware(LoggingMiddleware)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    logger.info("API Gateway starting up...")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"URL Service URL: {settings.url_service_url}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("API Gateway shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
