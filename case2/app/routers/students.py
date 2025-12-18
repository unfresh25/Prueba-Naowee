"""
Students Router (CRUD)
Endpoint to manage students
"""

import logging
from functools import lru_cache
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.schemas import StudentCreate, StudentResponse, StudentUpdate
from app.repositories.student_repository import StudentRepository
from app.services.model_loader import ModelLoader
from app.services.prediction_service import PredictionService
from app.services.student_service import StudentService

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/students",
    tags=["Students"],
)


@lru_cache()
def get_repository() -> StudentRepository:
    """Dependency injection for StudentRepository"""
    logger.info("Initializing StudentRepository")
    return StudentRepository()


def get_student_service(
    repository: StudentRepository = Depends(get_repository),
) -> StudentService:
    """Dependency injection for StudentService"""
    model_loader = ModelLoader()
    if not model_loader.is_loaded():
        raise HTTPException(
            status_code=503, detail="ML models not loaded. Service unavailable."
        )
    prediction_service = PredictionService(model_loader)
    return StudentService(repository, prediction_service)


@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create student",
    description="Creates a new student and generates prediction automatically",
)
async def create_student(
    student: StudentCreate, service: StudentService = Depends(get_student_service)
) -> StudentResponse:
    """
    Creates a new student with automatic prediction

    - Automatically generates a prediction when creating the student
    - The student_id must be unique
    """
    try:
        logger.info(f"Creating student: {student.student_id}")
        result = service.create_student(student)
        logger.info(f"Student {student.student_id} created successfully")
        return result

    except ValueError as e:
        logger.warning(f"Conflict creating student: {str(e)}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except Exception as e:
        logger.error(f"Error creating student: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating student: {str(e)}",
        )


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Get student",
    description="Get a student by ID",
)
async def get_student(
    student_id: str, service: StudentService = Depends(get_student_service)
) -> StudentResponse:
    """
    Get a student by ID
    """
    logger.info(f"Getting student: {student_id}")
    student = service.get_student(student_id)

    if student is None:
        logger.warning(f"Student {student_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student {student_id} not found",
        )

    return student


@router.get(
    "/",
    response_model=List[StudentResponse],
    summary="List students",
    description="Get all students",
)
async def list_students(
    service: StudentService = Depends(get_student_service),
) -> List[StudentResponse]:
    """
    List all students
    """
    logger.info("Listing all students")
    students = service.get_all_students()
    logger.info(f"Total of students: {len(students)}")
    return students


@router.put(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Update student",
    description="Update student data. Recalculate prediction if academic data changes",
)
async def update_student(
    student_id: str,
    update_data: StudentUpdate,
    service: StudentService = Depends(get_student_service),
) -> StudentResponse:
    """
    Update an existing student

    - If academic data is updated, the prediction is recalculated automatically
    - Fields not sent are kept unchanged
    """
    logger.info(f"Updating student {student_id}")
    student = service.update_student(student_id, update_data)

    if student is None:
        logger.warning(f"Student {student_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student {student_id} not found",
        )

    logger.info(f"Student {student_id} updated successfully")
    return student


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a student",
    description="Deletes a student by ID",
)
async def delete_student(
    student_id: str, service: StudentService = Depends(get_student_service)
):
    """
    Deletes a student by ID
    """
    logger.info(f"Deleting student {student_id}")
    deleted = service.delete_student(student_id)

    if not deleted:
        logger.warning(f"Student {student_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Student {student_id} not found",
        )

    logger.info(f"Student {student_id} deleted successfully")
    return None


@router.get(
    "/stats/summary",
    summary="Get system statistics",
    description="Gets system statistics",
)
async def get_statistics(
    service: StudentService = Depends(get_student_service),
) -> dict:
    """
    Gets system statistics

    - Total of students
    - Students at risk
    - Average performance
    """
    logger.info("Obteniendo estadísticas")
    stats = service.get_statistics()
    return stats
