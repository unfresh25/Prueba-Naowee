"""
Models Pydantic for data validation (DTOs)
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class StudentInput(BaseModel):
    """Data input for prediction"""

    hours_studied: float = Field(
        ..., ge=0, le=24, description="Hours of study per week"
    )
    previous_scores: float = Field(..., ge=0, le=100, description="Previous scores")
    extracurricular_activities: int = Field(
        ...,
        ge=0,
        le=1,
        description="Participation in extracurricular activities (0=No, 1=Yes)",
    )
    sleep_hours: float = Field(..., ge=0, le=24, description="Average sleep hours")
    sample_questions_practiced: int = Field(
        ..., ge=0, le=20, description="Sample questions practiced"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "hours_studied": 7.0,
                "previous_scores": 85.0,
                "extracurricular_activities": 1,
                "sleep_hours": 7.5,
                "sample_questions_practiced": 5,
            }
        }


class PredictionResponse(BaseModel):
    """Prediction response"""

    performance_index_predicted: float = Field(
        ..., description="Performance Index predicted (regression)"
    )
    low_performance_predicted: int = Field(
        ..., description="Prediction of low performance (0=No, 1=Yes)"
    )
    low_performance_probability: float = Field(
        ..., description="Probability of low performance"
    )
    risk_level: str = Field(..., description="Risk level (LOW, MEDIUM, HIGH)")


class StudentCreate(BaseModel):
    """Model for creating student"""

    student_id: str = Field(..., min_length=1, max_length=50)
    name: str = Field(..., min_length=1, max_length=100)
    input_data: StudentInput


class StudentUpdate(BaseModel):
    """Model for updating student"""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    input_data: Optional[StudentInput] = None


class StudentResponse(BaseModel):
    """Response for student data"""

    student_id: str
    name: str
    input_data: StudentInput
    prediction: Optional[PredictionResponse] = None
    created_at: datetime
    updated_at: datetime


class HealthResponse(BaseModel):
    """Response for health check"""

    status: str
    app_name: str
    version: str
    models_loaded: bool
    timestamp: datetime
