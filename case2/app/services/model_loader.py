"""
Service for loading ML models
"""

import logging
import os
from typing import Optional

import joblib

logger = logging.getLogger(__name__)


class ModelLoader:
    """
    Singleton for loading and managing ML models
    """

    _instance: Optional["ModelLoader"] = None
    _models_loaded: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._models_loaded:
            self.classification_model = None
            self.regression_model = None
            self.scaler = None
            self._models_loaded = False

    def load_models(
        self,
        models_path: str,
        classification_name: str,
        regression_name: str,
        scaler_name: str,
    ) -> bool:
        """
        Loads all necessary models

        Returns:
            bool: True if all models were loaded successfully
        """
        try:
            classification_path = os.path.join(models_path, classification_name)
            regression_path = os.path.join(models_path, regression_name)
            scaler_path = os.path.join(models_path, scaler_name)

            logger.info(f"Loading classification model from {classification_path}")
            self.classification_model = joblib.load(classification_path)

            logger.info(f"Loading regression model from {regression_path}")
            self.regression_model = joblib.load(regression_path)

            logger.info(f"Loading scaler from {scaler_path}")
            self.scaler = joblib.load(scaler_path)

            self._models_loaded = True
            logger.info("All models loaded successfully")
            return True

        except Exception as e:
            logger.error(f"Error loading models: {str(e)}")
            self._models_loaded = False
            return False

    def is_loaded(self) -> bool:
        """Verify if models are loaded"""
        return self._models_loaded

    def get_classification_model(self):
        """Return classification model"""
        if not self._models_loaded:
            raise RuntimeError("Models not loaded. Call load_models() first.")
        return self.classification_model

    def get_regression_model(self):
        """Return regression model"""
        if not self._models_loaded:
            raise RuntimeError("Models not loaded. Call load_models() first.")
        return self.regression_model

    def get_scaler(self):
        """Return scaler"""
        if not self._models_loaded:
            raise RuntimeError("Models not loaded. Call load_models() first.")
        return self.scaler
