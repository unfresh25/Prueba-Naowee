"""
App configuration
"""

from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """App configuration"""

    APP_NAME: str = "Student Performance API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "API for predicting student academic performance"

    MODELS_PATH: str = "./models"
    CLASSIFICATION_MODEL: str = "best_classification_model.pkl"
    REGRESSION_MODEL: str = "best_regression_model.pkl"
    SCALER_MODEL: str = "scaler.pkl"

    DEBUG: bool = False
    API_PREFIX: str = "/api/v1"

    class Config:
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Returns settings singleton"""
    return Settings()
