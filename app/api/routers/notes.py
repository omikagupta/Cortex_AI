from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.database import get_db
from app.schemas import (
    NoteCreate,
    NoteUpdate,
    NoteResponse,
)
from app.services import NoteService

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)

service = NoteService()


@router.post(
    "/{workspace_id}",
    response_model=NoteResponse,
    status_code=201,
)
def create_note(
    workspace_id: UUID,
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.create_note(
        db,
        workspace_id,
        note,
    )


@router.get(
    "/workspace/{workspace_id}",
    response_model=list[NoteResponse],
)
def get_notes(
    workspace_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.get_workspace_notes(
        db,
        workspace_id,
    )


@router.get(
    "/{note_id}",
    response_model=NoteResponse,
)
def get_note(
    note_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.get_note(
        db,
        note_id,
    )


@router.put(
    "/{note_id}",
    response_model=NoteResponse,
)
def update_note(
    note_id: UUID,
    note: NoteUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.update_note(
        db,
        note_id,
        note,
    )


@router.delete(
    "/{note_id}",
)
def delete_note(
    note_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.delete_note(
        db,
        note_id,
    )