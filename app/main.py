from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.api.v1.api import api_router
from app.core.config import settings
from app.services.model_service import model_service

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Model Path: {settings.MODEL_PATH}")
    logger.info(f"Model loaded: {model_service.model is not None}")
    
    if model_service.model is None:
        logger.error("CRITICAL: Model failed to load!")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")

# Create FastAPI app with enhanced metadata
# Conditionally disable docs in production for security (optional)
docs_url = None if settings.is_production else "/docs"
redoc_url = None if settings.is_production else "/redoc"
openapi_url = None if settings.is_production else f"{settings.API_V1_STR}/openapi.json"

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API for predicting breast cancer diagnosis using machine learning",
    openapi_url=openapi_url,
    docs_url=docs_url,
    redoc_url=redoc_url,
    lifespan=lifespan
)

# CORS Configuration
allowed_origins = settings.ALLOWED_ORIGINS

# For development, you might want to allow all origins
if settings.ENVIRONMENT == "development" and "*" not in allowed_origins:
    logger.warning("Development mode: Consider adding '*' to ALLOWED_ORIGINS for easier testing")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)

# Root endpoint
@app.get(
    "/",
    tags=["Root"],
    summary="API Root",
    response_description="Welcome message and API information"
)
def root():
    """
    Root endpoint providing basic API information and navigation
    """
    response = {
        "message": "Welcome to the Breast Cancer Prediction API",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "health": f"{settings.API_V1_STR}/system/health",
        "api_version": settings.API_V1_STR
    }
    
    # Only include docs URL in development
    if not settings.is_production:
        response["docs"] = "/docs"
        response["redoc"] = "/redoc"
    
    return response