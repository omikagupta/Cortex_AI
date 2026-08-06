from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import Note
from app.repositories import NoteRepository
from app.schemas import (
    NoteCreate,
    NoteUpdate,
)


class NoteService:

    def __init__(self):
        self.repository = NoteRepository()

    def create_note(
        self,
        db: Session,
        workspace_id,
        note_data: NoteCreate,
    ):
        note = Note(
            title=note_data.title,
            content=note_data.content,
            workspace_id=workspace_id,
        )

        return self.repository.create(
            db,
            note,
        )

    def get_workspace_notes(
        self,
        db: Session,
        workspace_id,
    ):
        return self.repository.get_all_by_workspace(
            db,
            workspace_id,
        )

    def get_note(
        self,
        db: Session,
        note_id,
    ):
        note = self.repository.get_by_id(
            db,
            note_id,
        )

        if note is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found",
            )

        return note

    def update_note(
        self,
        db: Session,
        note_id,
        note_data: NoteUpdate,
    ):
        note = self.repository.get_by_id(
            db,
            note_id,
        )

        if note is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found",
            )

        note.title = note_data.title
        note.content = note_data.content

        return self.repository.update(
            db,
            note,
        )

    def delete_note(
        self,
        db: Session,
        note_id,
    ):
        note = self.repository.get_by_id(
            db,
            note_id,
        )

        if note is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Note not found",
            )

        self.repository.delete(
            db,
            note,
        )

        return {
            "message": "Note deleted successfully"
        }