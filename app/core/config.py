from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os

class Settings(BaseSettings):
    # 1. Project Metadata 
    PROJECT_NAME: str = 'Breast Cancer Prediction API'
    VERSION: str = '1.0.0'
    API_V1_STR: str = '/api/v1'

    # 2. ML Model Settings
    # This will use environment variable if set, otherwise default
    MODEL_PATH: str = 'models/model_v1.pkl'

    # 3. CORS Settings
    # Allow Streamlit and common frontend frameworks
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",  # React default
        "http://localhost:8501",  # Streamlit default
        "http://localhost:5173",  # Vite default
        "https://*.streamlit.app",  # Streamlit Cloud (all subdomains)
        # Add your production frontend URL after deploying
    ]

    # 4. Environment
    ENVIRONMENT: str = "development"  # Options: "development", "production"
    
    # 5. Server Configuration
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = "0.0.0.0"

    # 6. Pydantic Configuration
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=True 
    )
    
    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.ENVIRONMENT.lower() == "production"

# Instantiate the settings object to be used across the app
settings = Settings()