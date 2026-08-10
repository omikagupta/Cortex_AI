from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    id: UUID
    filename: str
    file_path: str
    file_size: int
    content_type: str
    extracted_text: str | None
    status: str
    workspace_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)