from datetime import datetime

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: str
    timestamp: datetime