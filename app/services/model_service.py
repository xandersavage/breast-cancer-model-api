import pickle
import pandas as pd
from typing import Tuple, Protocol
from numpy.typing import NDArray
from app.core.config import settings

# Define what a "model" looks like to the type checker
class SklearnModel(Protocol):
    def predict(self, X: pd.DataFrame) -> NDArray:
        ...
    
    def predict_proba(self, X: pd.DataFrame) -> NDArray:
        ...

class ModelService:
    def __init__(self):
        self.model: SklearnModel | None = None
        self._load_model()

    def _load_model(self) -> None:
        """
        Loads the pickle file into memory
        """
        try:
            with open(settings.MODEL_PATH, "rb") as f:
                self.model = pickle.load(f)
                print("Model loaded successfully")
        except FileNotFoundError:
            print(f"Model file not found at {settings.MODEL_PATH}")
            raise
        except Exception as e:
            print(f"Error loading model: {e}")
            raise

    def predict(self, input_data) -> Tuple[str, float]:
        """
        Makes prediction on input data
        
        Args:
            input_data: Pydantic model with cancer features
            
        Returns:
            Tuple of (prediction label, probability)
            
        Raises:
            RuntimeError: If model is not loaded
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Cannot make predictions.")
        
        # Convert Pydantic model to DataFrame
        data_df = pd.DataFrame([input_data.model_dump()])  # Pydantic v2
        # Use input_data.dict() for Pydantic v1

        prediction = self.model.predict(data_df)
        probability = self.model.predict_proba(data_df)[:, 1]

        result = 'Malignant' if prediction[0] == 1 else 'Benign'

        return result, float(probability[0])
    
# Create a singleton instance 
model_service = ModelService()