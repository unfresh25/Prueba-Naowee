import logging
from contextlib import asynccontextmanager
from datetime import datetime

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import get_settings
from app.models.schemas import HealthResponse
from app.routers import prediction, students
from app.services.model_loader import ModelLoader

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events - Load models
    """
    model_loader = ModelLoader()
    success = model_loader.load_models(
        models_path=settings.MODELS_PATH,
        classification_name=settings.CLASSIFICATION_MODEL,
        regression_name=settings.REGRESSION_MODEL,
        scaler_name=settings.SCALER_MODEL,
    )

    if not success:
        logger.error("Error loading ML models")
        raise RuntimeError("Could not load ML models")

    logger.info("API ready to receive requests")

    yield

    logger.info("Closing API...")


app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    logger.error(f"Not captured: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc) if settings.DEBUG else "Internal server error",
        },
    )


app.include_router(prediction.router, prefix=settings.API_PREFIX)
app.include_router(students.router, prefix=settings.API_PREFIX)


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health Check",
    description="Verify API and models",
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint
    """
    model_loader = ModelLoader()

    return HealthResponse(
        status="healthy" if model_loader.is_loaded() else "unhealthy",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        models_loaded=model_loader.is_loaded(),
        timestamp=datetime.now(),
    )


@app.get(
    "/",
    tags=["Root"],
    summary="Root endpoint",
    description="Basic information about the API",
)
async def root():
    """
    Endpoint root with API information
    """
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": settings.APP_DESCRIPTION,
        "docs": "/docs",
        "health": "/health",
        "api_prefix": settings.API_PREFIX,
        "endpoints": {
            "predictions": f"{settings.API_PREFIX}/predictions",
            "students": f"{settings.API_PREFIX}/students",
            "health": "/health",
        },
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG, log_level="info"
    )
