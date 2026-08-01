from fastapi import FastAPI

from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.core.logging import logger

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

register_exception_handlers(app)


@app.on_event("startup")
async def startup_event():
    logger.info("AI Workspace Agent started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("AI Workspace Agent stopped")