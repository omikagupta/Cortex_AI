from sqlalchemy.orm import Session

from app.models import Workspace


class WorkspaceRepository:

    def create(
        self,
        db: Session,
        workspace: Workspace,
    ) -> Workspace:
        db.add(workspace)
        db.commit()
        db.refresh(workspace)
        return workspace

    def get_all_by_owner(
        self,
        db: Session,
        owner_id,
    ):
        return (
            db.query(Workspace)
            .filter(Workspace.owner_id == owner_id)
            .all()
        )