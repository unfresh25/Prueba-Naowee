"""
Prediction Service
"""

import logging
from typing import List

import numpy as np
import pandas as pd

from app.models.schemas import PredictionResponse, StudentInput
from app.services.model_loader import ModelLoader

logger = logging.getLogger(__name__)


class PredictionService:
    """
    Service for making predictions using ML models
    """

    def __init__(self, model_loader: ModelLoader):
        """
        Initializes the service with the model loader

        Args:
            model_loader: Instance of ModelLoader
        """
        self.model_loader = model_loader

    def _prepare_features(self, student_input: StudentInput) -> np.ndarray:
        """
        Prepares the features for the model

        Args:
            student_input: Data of the student

        Returns:
            Array numpy with scaled features
        """
        feature_names = [
            "Hours Studied",
            "Previous Scores",
            "Extracurricular Activities",
            "Sleep Hours",
            "Sample Question Papers Practiced",
        ]

        features_dict = {
            "Hours Studied": student_input.hours_studied,
            "Previous Scores": student_input.previous_scores,
            "Extracurricular Activities": student_input.extracurricular_activities,
            "Sleep Hours": student_input.sleep_hours,
            "Sample Question Papers Practiced": student_input.sample_questions_practiced,
        }

        features_df = pd.DataFrame([features_dict], columns=feature_names)

        scaler = self.model_loader.get_scaler()
        features_scaled = scaler.transform(features_df)

        return features_scaled

    def predict(self, student_input: StudentInput) -> PredictionResponse:
        """
        Make predictions for a student

        Args:
            student_input: Student input data

        Returns:
            PredictionResponse with predictions
        """
        try:
            features_scaled = self._prepare_features(student_input)

            regression_model = self.model_loader.get_regression_model()
            performance_predicted = float(regression_model.predict(features_scaled)[0])

            classification_model = self.model_loader.get_classification_model()
            low_performance_predicted = int(
                classification_model.predict(features_scaled)[0]
            )

            if hasattr(classification_model, "predict_proba"):
                proba = classification_model.predict_proba(features_scaled)[0]
                low_performance_probability = float(proba[1])
            else:
                low_performance_probability = float(low_performance_predicted)

            if low_performance_predicted == 1:
                if low_performance_probability >= 0.8:
                    risk_level = "HIGH"
                elif low_performance_probability >= 0.6:
                    risk_level = "MEDIUM-HIGH"
                else:
                    risk_level = "MEDIUM-LOW"
            else:
                risk_level = "LOW"

            return PredictionResponse(
                performance_index_predicted=round(performance_predicted, 2),
                low_performance_predicted=low_performance_predicted,
                low_performance_probability=round(low_performance_probability, 4),
                risk_level=risk_level,
            )

        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            raise RuntimeError(f"Prediction error: {str(e)}")
