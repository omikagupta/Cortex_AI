from pathlib import Path
import shutil

import fitz
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models import Document
from app.repositories import DocumentRepository


UPLOAD_DIR = Path("app/storage/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class DocumentService:

    def __init__(self):
        self.repository = DocumentRepository()

    def extract_pdf_text(self, file_path: Path) -> str:
        """
        Extract text from a PDF using PyMuPDF.
        """

        text = []

        with fitz.open(file_path) as pdf:
            for page in pdf:
                page_text = page.get_text()

                if page_text:
                    text.append(page_text)

        return "\n".join(text).strip()

    def upload_document(
        self,
        db: Session,
        workspace_id,
        file: UploadFile,
    ):
        file_path = UPLOAD_DIR / file.filename

        # Save uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        extracted_text = None

        # Extract text from PDF
        if file.content_type == "application/pdf":
            extracted_text = self.extract_pdf_text(file_path)

        document = Document(
            filename=file.filename,
            file_path=str(file_path),
            file_size=file_path.stat().st_size,
            content_type=file.content_type,
            extracted_text=extracted_text,
            workspace_id=workspace_id,
        )

        return self.repository.create(
            db,
            document,
        )

    def get_documents(
        self,
        db: Session,
        workspace_id,
    ):
        return self.repository.get_by_workspace(
            db,
            workspace_id,
        )