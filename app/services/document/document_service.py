import shutil
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models import Document
from app.repositories.document_repository import DocumentRepository
from app.services.chunking.document_chunk_service import DocumentChunkService
from app.services.document.text_extractor import TextExtractor


# =========================================
# Upload directory
# =========================================

UPLOAD_DIR = Path("app/storage/uploads")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


class DocumentService:

    def __init__(self):
        self.repository = DocumentRepository()
        self.chunk_service = DocumentChunkService()
        self.text_extractor = TextExtractor()

    def upload_document(
        self,
        db: Session,
        workspace_id,
        file: UploadFile,
    ):

        print("\n========================================")
        print("DOCUMENT UPLOAD STARTED")
        print("========================================")

        print("Filename:", file.filename)
        print("Content Type:", file.content_type)

        # =========================================
        # 1. Save uploaded file
        # =========================================

        file_path = UPLOAD_DIR / file.filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        print("File saved:", file_path)
        print("File size:", file_path.stat().st_size)

        # =========================================
        # 2. Extract text
        # =========================================

        extracted_text = None
        status = "UPLOADED"

        print("\n========================================")
        print("STARTING TEXT EXTRACTION")
        print("========================================")

        try:

            extracted_text = self.text_extractor.extract(
                str(file_path),
                file.content_type,
            )

            print("EXTRACTION COMPLETED")

            print(
                "Extracted text length:",
                len(extracted_text)
                if extracted_text
                else 0,
            )

            print("First 200 characters:")

            print(
                extracted_text[:200]
                if extracted_text
                else "NO TEXT",
            )

            if extracted_text:
                status = "PROCESSED"
            else:
                status = "FAILED"

        except Exception as e:

            print("\n========================================")
            print("EXTRACTION FAILED")
            print("ERROR:", repr(e))
            print("========================================")

            extracted_text = None
            status = "FAILED"

        # =========================================
        # 3. Create Document object
        # =========================================

        document = Document(
            filename=file.filename,
            file_path=str(file_path),
            file_size=file_path.stat().st_size,
            content_type=file.content_type,
            extracted_text=extracted_text,
            status=status,
            workspace_id=workspace_id,
        )

        # =========================================
        # 4. Save Document
        # =========================================

        print("\nSaving document to database...")

        result = self.repository.create(
            db,
            document,
        )

        print("DATABASE SAVE COMPLETED")
        print("Document ID:", result.id)

        # =========================================
        # 5. Create chunks + embeddings
        # =========================================

        if extracted_text and status == "PROCESSED":

            print("\n========================================")
            print("STARTING CHUNKING + EMBEDDINGS")
            print("========================================")

            try:

                chunks = self.chunk_service.create_chunks(
                    db=db,
                    document_id=result.id,
                    text=extracted_text,
                )

                print("\n========================================")
                print("CHUNKS CREATED")
                print("TOTAL CHUNKS:", len(chunks))
                print("========================================")

            except Exception as e:

                print("\n========================================")
                print("CHUNKING / EMBEDDING FAILED")
                print("ERROR:", repr(e))
                print("========================================")

        # =========================================
        # 6. Finish
        # =========================================

        print("\n========================================")
        print("DOCUMENT UPLOAD FINISHED")
        print("========================================")

        print("Document ID:", result.id)
        print("Status:", result.status)

        print(
            "Extracted text:",
            result.extracted_text is not None,
        )

        print("========================================\n")

        return result

    def get_documents(
        self,
        db: Session,
        workspace_id,
    ):

        return self.repository.get_by_workspace(
            db,
            workspace_id,
        )