"""
Students Service
"""

import logging
from typing import List, Optional

from app.models.schemas import (
    StudentCreate,
    StudentInput,
    StudentResponse,
    StudentUpdate,
)
from app.repositories.student_repository import StudentRepository
from app.services.prediction_service import PredictionService

logger = logging.getLogger(__name__)


class StudentService:
    """
    Service to manage student operations
    """

    def __init__(
        self, repository: StudentRepository, prediction_service: PredictionService
    ):
        """
        Initialize the service

        Args:
            repository: Student repository
            prediction_service: Prediction service
        """
        self.repository = repository
        self.prediction_service = prediction_service

    def create_student(self, student_data: StudentCreate) -> StudentResponse:
        """
        Create a new student with automatic prediction

        Args:
            student_data: Data of the student

        Returns:
            StudentResponse with data and prediction

        Raises:
            ValueError: If the student already exists
        """
        if self.repository.exists(student_data.student_id):
            raise ValueError(
                f"Student with ID {student_data.student_id} already exists"
            )

        prediction = self.prediction_service.predict(student_data.input_data)

        student_dict = self.repository.create(
            student_id=student_data.student_id,
            name=student_data.name,
            input_data=student_data.input_data,
            prediction=prediction,
        )

        logger.info(f"Student {student_data.student_id} created with prediction")

        return self._dict_to_response(student_dict)

    def get_student(self, student_id: str) -> Optional[StudentResponse]:
        """
        Get student by ID

        Args:
            student_id: ID of the student

        Returns:
            StudentResponse or None if not found
        """
        student_dict = self.repository.get_by_id(student_id)

        if student_dict is None:
            return None

        return self._dict_to_response(student_dict)

    def get_all_students(self) -> List[StudentResponse]:
        """
        Get all students

        Returns:
            List of StudentResponse
        """
        students_dict = self.repository.get_all()
        return [self._dict_to_response(s) for s in students_dict]

    def update_student(
        self, student_id: str, update_data: StudentUpdate
    ) -> Optional[StudentResponse]:
        """
        Update a student and recalculate prediction if new data is available

        Args:
            student_id: ID of the student
            update_data: Data to update

        Returns:
            StudentResponse updated or None if not exists
        """
        if not self.repository.exists(student_id):
            return None

        prediction = None
        if update_data.input_data is not None:
            prediction = self.prediction_service.predict(update_data.input_data)

        student_dict = self.repository.update(
            student_id=student_id,
            name=update_data.name,
            input_data=update_data.input_data,
            prediction=prediction,
        )

        logger.info(f"Student {student_id} updated")

        return self._dict_to_response(student_dict)

    def delete_student(self, student_id: str) -> bool:
        """
        Deletes a student

        Args:
            student_id: ID of the student

        Returns:
            True if deleted, False if not exists
        """
        deleted = self.repository.delete(student_id)

        if deleted:
            logger.info(f"Student {student_id} deleted")

        return deleted

    def get_statistics(self) -> dict:
        """
        Gets general statistics

        Returns:
            Dict with statistics
        """
        all_students = self.repository.get_all()

        if not all_students:
            return {
                "total_students": 0,
                "students_at_risk": 0,
                "risk_percentage": 0.0,
                "average_performance": 0.0,
            }

        students_at_risk = sum(
            1
            for s in all_students
            if s.get("prediction") and s["prediction"]["low_performance_predicted"] == 1
        )

        performances = [
            s["prediction"]["performance_index_predicted"]
            for s in all_students
            if s.get("prediction")
        ]

        avg_performance = sum(performances) / len(performances) if performances else 0.0

        return {
            "total_students": len(all_students),
            "students_at_risk": students_at_risk,
            "risk_percentage": round((students_at_risk / len(all_students)) * 100, 2),
            "average_performance": round(avg_performance, 2),
        }

    def _dict_to_response(self, student_dict: dict) -> StudentResponse:
        """
        Converts dict to StudentResponse

        Args:
            student_dict: Dictionary with student data

        Returns:
            StudentResponse
        """
        return StudentResponse(
            student_id=student_dict["student_id"],
            name=student_dict["name"],
            input_data=StudentInput(**student_dict["input_data"]),
            prediction=student_dict.get("prediction"),
            created_at=student_dict["created_at"],
            updated_at=student_dict["updated_at"],
        )
