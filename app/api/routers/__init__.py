from app.api.routers.health import router as health_router
from app.api.routers.users import router as users_router
from app.api.routers.auth import router as auth_router
from app.api.routers.workspaces import router as workspaces_router

__all__ = [
    "health_router",
    "users_router",
    "auth_router",
    "workspaces_router",
]
