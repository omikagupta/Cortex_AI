from datetime import datetime

from fastapi import APIRouter, status

from app.core.config import settings
from app.schemas.api_response import ApiResponse
from app.schemas.health import HealthResponse
from app.utils.response import success_response

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[HealthResponse],
    summary="Health Check",
    description="Returns the health status of the application.",
)
def health_check():
    health = HealthResponse(
        status="healthy",
        application=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        timestamp=datetime.utcnow(),
    )

    return success_response(
        message="Application is healthy",
        data=health,
    )