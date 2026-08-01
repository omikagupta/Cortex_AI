from datetime import datetime
from typing import Any

from app.schemas.api_response import ApiResponse


def success_response(
    message: str,
    data: Any = None,
) -> ApiResponse:
    """
    Standard success response.
    """
    return ApiResponse(
        success=True,
        message=message,
        data=data,
        timestamp=datetime.utcnow(),
    )