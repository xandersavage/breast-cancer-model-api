from pydantic import BaseModel, Field

class CancerInput(BaseModel):
    # Field allows us to add metadata and validation
    radius_mean: float = Field(gt=0, description='Mean of distances from center to points on the perimeter', examples=[17.99])
    texture_mean: float = Field(gt=0, examples=[10.38])
    perimeter_mean: float = Field(gt=0, examples=[122.8])
    smoothness_mean: float = Field(gt=0, examples=[0.2776])
    compactness_mean: float = Field(gt=0, examples=[0.2776])

class CancerPredictionResponse(BaseModel):
    prediction: str
    probability: float
    status: str = 'success'