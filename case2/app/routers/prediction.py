"""
Prediction Router
Endpoint for making academic performance predictions
"""

import logging

from fastapi import APIRouter, Depends, HTTPException

from app.models.schemas import PredictionResponse, StudentInput
from app.services.model_loader import ModelLoader
from app.services.prediction_service import PredictionService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"],
)


def get_prediction_service() -> PredictionService:
    """Dependency injection for PredictionService"""
    model_loader = ModelLoader()
    if not model_loader.is_loaded():
        raise HTTPException(
            status_code=503, detail="ML models are not loaded. Service unavailable."
        )
    return PredictionService(model_loader)


@router.post(
    "/",
    response_model=PredictionResponse,
    summary="Make prediction",
    description="Predicts academic performance of a student based on their characteristics",
)
async def predict_performance(
    student_input: StudentInput,
    prediction_service: PredictionService = Depends(get_prediction_service),
) -> PredictionResponse:
    """
    Makes academic performance prediction

    - **hours_studied**: Hours of study per week (0-24)
    - **previous_scores**: Previous academic scores (0-100)
    - **extracurricular_activities**: Participation in activities (0=No, 1=Yes)
    - **sleep_hours**: Average sleep hours (0-24)
    - **sample_questions_practiced**: Sample questions practiced (0-20)

    Returns:
    - Performance Index predicted
    - Risk Classification
    - Probability of Low Performance
    """
    try:
        logger.info("Prediction request received")
        prediction = prediction_service.predict(student_input)
        logger.info(f"Prediction successful: Risk={prediction.risk_level}")
        return prediction

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Error predicting performance: {str(e)}"
        )


@router.post(
    "/batch",
    response_model=list[PredictionResponse],
    summary="Batch Prediction",
    description="Make predictions for multiple students",
)
async def predict_batch(
    students: list[StudentInput],
    prediction_service: PredictionService = Depends(get_prediction_service),
) -> list[PredictionResponse]:
    """
    Make predictions for multiple students
    """
    try:
        logger.info(f"Batch prediction request received: {len(students)} students")

        predictions = []
        for student in students:
            prediction = prediction_service.predict(student)
            predictions.append(prediction)

        logger.info(f"Batch prediction successful: {len(predictions)} results")
        return predictions

    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Batch prediction error: {str(e)}")
