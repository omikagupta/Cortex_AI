from sqlalchemy.orm import Session

from app.models import Note


class NoteRepository:

    def create(
        self,
        db: Session,
        note: Note,
    ) -> Note:
        db.add(note)
        db.commit()
        db.refresh(note)
        return note

    def get_all_by_workspace(
        self,
        db: Session,
        workspace_id,
    ):
        return (
            db.query(Note)
            .filter(Note.workspace_id == workspace_id)
            .all()
        )

    def get_by_id(
        self,
        db: Session,
        note_id,
    ):
        return (
            db.query(Note)
            .filter(Note.id == note_id)
            .first()
        )

    def update(
        self,
        db: Session,
        note: Note,
    ):
        db.commit()
        db.refresh(note)
        return note

    def delete(
        self,
        db: Session,
        note: Note,
    ):
        db.delete(note)
        db.commit()