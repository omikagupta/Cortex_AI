from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    filename: str
    file_path: str
    file_size: int
    content_type: str
    extracted_text: str | None
    workspace_id: UUID
    created_at: datetime
    updated_at: datetime