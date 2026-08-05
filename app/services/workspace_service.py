from sqlalchemy.orm import Session

from app.models import Workspace
from app.repositories import WorkspaceRepository
from app.schemas import WorkspaceCreate


class WorkspaceService:

    def __init__(self):
        self.repository = WorkspaceRepository()

    def create_workspace(
        self,
        db: Session,
        workspace_data: WorkspaceCreate,
        owner_id,
    ):
        workspace = Workspace(
            name=workspace_data.name,
            description=workspace_data.description,
            owner_id=owner_id,
        )

        return self.repository.create(
            db,
            workspace,
        )

    def get_user_workspaces(
        self,
        db: Session,
        user_id,
    ):
        return self.repository.get_all_by_owner(
            db,
            user_id,
        )