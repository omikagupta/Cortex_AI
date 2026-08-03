from fastapi import FastAPI

from app.api.routers import (
    health_router,
    users_router,
)
from app.api.routers import (
    health_router,
    users_router,
    auth_router,
)

from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.core.logging import logger

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=True,
)

register_exception_handlers(app)

app.include_router(
    health_router,
    prefix=settings.API_V1_PREFIX,
)


app.include_router(
    users_router,
    prefix=settings.API_V1_PREFIX,
)
app.include_router(
    auth_router,
    prefix=settings.API_V1_PREFIX,
)

print("REGISTERED ROUTES:")
for route in app.routes:
    print(route.path)