from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.database import get_db
from app.schemas import (
    WorkspaceCreate,
    WorkspaceResponse,
)
from app.services import WorkspaceService

router = APIRouter(
    prefix="/workspaces",
    tags=["Workspaces"],
)

service = WorkspaceService()


@router.post(
    "",
    response_model=WorkspaceResponse,
    status_code=201,
)
def create_workspace(
    workspace: WorkspaceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.create_workspace(
        db,
        workspace,
        current_user.id,
    )


@router.get(
    "",
    response_model=list[WorkspaceResponse],
)
def get_my_workspaces(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.get_user_workspaces(
        db,
        current_user.id,
    )