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

    def get_by_id(
        self,
        db: Session,
        workspace_id,
    ):
        return (
            db.query(Workspace)
            .filter(Workspace.id == workspace_id)
            .first()
        )

    def get_by_id_and_owner(
        self,
        db: Session,
        workspace_id,
        owner_id,
    ):
        return (
            db.query(Workspace)
            .filter(
                Workspace.id == workspace_id,
                Workspace.owner_id == owner_id,
            )
            .first()
        )

    def update(
        self,
        db: Session,
        workspace: Workspace,
    ):
        db.commit()
        db.refresh(workspace)
        return workspace

    def delete(
        self,
        db: Session,
        workspace: Workspace,
    ):
        db.delete(workspace)
        db.commit()