from fastapi import APIRouter
from app.api.v1.endpoints import health, prediction

api_router = APIRouter()

# System endpoints (health, metrics, etc.)
api_router.include_router(
    health.router,
    tags=["System"],
    prefix="/system"  # Routes become /system/health
)

# ML Model endpoints
api_router.include_router(
    prediction.router,
    tags=["Machine Learning"],
    prefix="/ml"  # Routes become /ml/predict
)