from datetime import datetime
import traceback

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException
from app.core.logging import logger
from app.schemas.error_response import ErrorResponse


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger.warning(
            f"{request.method} {request.url.path} - {exc.error_code}: {exc.message}"
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                message=exc.message,
                error_code=exc.error_code,
                timestamp=datetime.utcnow(),
            ).model_dump(mode="json"),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        logger.warning(
            f"{request.method} {request.url.path} - Validation Error - {exc.errors()}"
        )

        return JSONResponse(
            status_code=422,
            content=ErrorResponse(
                message="Validation failed",
                error_code="VALIDATION_ERROR",
                timestamp=datetime.utcnow(),
            ).model_dump(mode="json"),
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ):
        logger.warning(
            f"{request.method} {request.url.path} - HTTP {exc.status_code}: {exc.detail}"
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=ErrorResponse(
                message=str(exc.detail),
                error_code="HTTP_ERROR",
                timestamp=datetime.utcnow(),
            ).model_dump(mode="json"),
        )

    @app.exception_handler(Exception)
    async def unexpected_exception_handler(
        request: Request,
        exc: Exception,
    ):
        print("\n" + "=" * 80)
        print("UNHANDLED EXCEPTION")
        traceback.print_exception(type(exc), exc, exc.__traceback__)
        print("=" * 80 + "\n")

        logger.exception("Unhandled exception")

        return JSONResponse(
            status_code=500,
            content={
                "message": str(exc),
                "type": type(exc).__name__,
            },
        )