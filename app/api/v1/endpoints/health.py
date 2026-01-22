from fastapi import APIRouter, status
from app.core.config import settings
from app.services.model_service import model_service

router = APIRouter()

@router.get('/health', status_code=status.HTTP_200_OK)
def health_check():
    """
    Health check endpoint to verify API is running
    """
    model_loaded = model_service.model is not None

    return {
        "status": "healthy" if model_loaded else "degraded",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "model_loaded": model_loaded
    }