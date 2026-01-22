from fastapi import APIRouter, HTTPException, status
from app.models.cancer import CancerInput, CancerPredictionResponse
from app.services.model_service import model_service
import logging

# Set up logger 
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post(
    '/predict',
    response_model=CancerPredictionResponse,
    status_code=status.HTTP_200_OK,
    summary='Predict cancer diagnosis',
    description="Predict whether a tumor is benign or malignant based on cell nucleus features"
)
def predict_cancer(payload: CancerInput):
    """
    Predict cancer diagnosis from tumor measurements
    
    Args:
        payload: Input features including radius_mean, texture_mean, etc.
        
    Returns:
        CancerPredictionResponse: Prediction result with probability
        
    Raises:
        HTTPException: 503 if model not loaded, 500 if prediction fails
    """
    # Check if model is loaded 
    if model_service.model is None:
        logger.error('Prediction attempted but model is not loaded')
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model not available. Service is starting up or experiencing issues."
        )
    try:
        prediction, probability = model_service.predict(payload)

        logger.info(f"Prediction successful: {prediction} (probability: {probability:.4f})")

        return CancerPredictionResponse(
            prediction=prediction,
            probability=probability,
            status='success'
        )
    except ValueError as e:
        # Specific error for invalid input data 
        logger.warning(f"Invalid input data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=f"Invalid input data: {str(e)}"
        )
    except Exception as e:
        # Generic error handler
        logger.error(f"Prediction failed with unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during prediction. Please try again."
        )


