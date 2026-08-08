from fastapi import FastAPI

from app.api.routers import (
    health_router,
    users_router,
    auth_router,
    workspaces_router,
    notes_router,
    documents_router,
)

from app.core.config import settings
from app.core.exception_handlers import register_exception_handlers
from app.core.logging import logger

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=True,
)

# Register exception handlers
register_exception_handlers(app)

# Register routers
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

app.include_router(
    workspaces_router,
    prefix=settings.API_V1_PREFIX,
)

app.include_router(
    notes_router,
    prefix=settings.API_V1_PREFIX,
)
print("INCLUDING DOCUMENTS ROUTER")
app.include_router(
    documents_router,
    prefix=settings.API_V1_PREFIX,
)

# Print all registered routes
logger.info("Registered Routes:")

print("\n========== REGISTERED ROUTES ==========")
for route in app.routes:
    print(route.path)
print("=======================================\n")