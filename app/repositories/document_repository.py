from sqlalchemy.orm import Session

from app.models import Document


class DocumentRepository:

    def create(
        self,
        db: Session,
        document: Document,
    ) -> Document:
        db.add(document)
        db.commit()
        db.refresh(document)
        return document

    def get_by_workspace(
        self,
        db: Session,
        workspace_id,
    ):
        return (
            db.query(Document)
            .filter(Document.workspace_id == workspace_id)
            .all()
        )

    def get_by_id(
        self,
        db: Session,
        document_id,
    ):
        return (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

    def delete(
        self,
        db: Session,
        document: Document,
    ):
        db.delete(document)
        db.commit()