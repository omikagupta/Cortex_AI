from fastapi import FastAPI

from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

register_exception_handlers(app)