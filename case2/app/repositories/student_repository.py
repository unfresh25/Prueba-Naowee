"""
Students Repository
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional

from app.models.schemas import PredictionResponse, StudentInput

logger = logging.getLogger(__name__)


class StudentRepository:
    """
    Repository for managing students in memory (simulates DB)
    Principle: Dependency Inversion - Could implement an IRepository interface
    """

    def __init__(self):
        """Initialize the repository on memory"""
        self._students: Dict[str, dict] = {}
        logger.info("StudentRepository initialized")

    def create(
        self,
        student_id: str,
        name: str,
        input_data: StudentInput,
        prediction: Optional[PredictionResponse] = None,
    ) -> dict:
        """
        Creates a new student

        Args:
            student_id: Unique student ID
            name: Student name
            input_data: Academic data
            prediction: Prediction (optional)

        Returns:
            dict with student data

        Raises:
            ValueError: If student_id already exists
        """
        if student_id in self._students:
            raise ValueError(f"Student with ID {student_id} already exists")

        student_data = {
            "student_id": student_id,
            "name": name,
            "input_data": input_data.model_dump(),
            "prediction": prediction.model_dump() if prediction else None,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }

        self._students[student_id] = student_data
        logger.info(f"Student {student_id} created successfully")

        return student_data

    def get_by_id(self, student_id: str) -> Optional[dict]:
        """
        Gets a student by ID

        Args:
            student_id: ID of the student

        Returns:
            dict with student data or None if not found
        """
        return self._students.get(student_id)

    def get_all(self) -> List[dict]:
        """
        Gets all students

        Returns:
            List of students
        """
        return list(self._students.values())

    def update(
        self,
        student_id: str,
        name: Optional[str] = None,
        input_data: Optional[StudentInput] = None,
        prediction: Optional[PredictionResponse] = None,
    ) -> Optional[dict]:
        """
        Updates an existing student

        Args:
            student_id: ID of the student
            name: New name (optional)
            input_data: New academic data (optional)
            prediction: New prediction (optional)

        Returns:
            dict with updated data or None if not found
        """
        if student_id not in self._students:
            return None

        student = self._students[student_id]

        if name is not None:
            student["name"] = name

        if input_data is not None:
            student["input_data"] = input_data.model_dump()

        if prediction is not None:
            student["prediction"] = prediction.model_dump()

        student["updated_at"] = datetime.now()

        logger.info(f"Student {student_id} updated")
        return student

    def delete(self, student_id: str) -> bool:
        """
        Deletes a student

        Args:
            student_id: ID of the student

        Returns:
            True if deleted, False if not found
        """
        if student_id in self._students:
            del self._students[student_id]
            logger.info(f"Student {student_id} deleted")
            return True
        return False

    def exists(self, student_id: str) -> bool:
        """
        Verifies if a student exists

        Args:
            student_id: ID of the student

        Returns:
            True if exists, False if not
        """
        return student_id in self._students

    def count(self) -> int:
        """
        Counts the total number of students

        Returns:
            Total number of students
        """
        return len(self._students)
