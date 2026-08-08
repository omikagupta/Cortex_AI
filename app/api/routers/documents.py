from uuid import UUID

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.database import get_db
from app.schemas import DocumentResponse
from app.services import DocumentService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

service = DocumentService()


@router.post(
    "/upload/{workspace_id}",
    response_model=DocumentResponse,
    status_code=201,
)
def upload_document(
    workspace_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.upload_document(
        db,
        workspace_id,
        file,
    )


@router.get(
    "/workspace/{workspace_id}",
    response_model=list[DocumentResponse],
)
def get_documents(
    workspace_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return service.get_documents(
        db,
        workspace_id,
    )