from pathlib import Path
import shutil

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models import Document
from app.repositories import DocumentRepository
from app.services.extractors.extractor_factory import get_extractor
from app.services.chunking.document_chunk_service import DocumentChunkService


UPLOAD_DIR = Path("app/storage/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


class DocumentService:

    def __init__(self):
        self.repository = DocumentRepository()
        self.chunk_service = DocumentChunkService()

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

        # -----------------------------------------
        # 1. Save file
        # -----------------------------------------

        file_path = UPLOAD_DIR / file.filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("File saved:", file_path)
        print("File size:", file_path.stat().st_size)

        # -----------------------------------------
        # 2. Find extractor
        # -----------------------------------------

        extractor = get_extractor(file.filename)

        print("Extractor:", extractor)

        extracted_text = None
        status = "UPLOADED"

        # -----------------------------------------
        # 3. Extract text
        # -----------------------------------------

        if extractor:

            print("\n========================================")
            print("EXTRACTOR FOUND")
            print("========================================")

            try:

                extracted_text = extractor(
                    str(file_path)
                )

                print("EXTRACTION COMPLETED")

                print(
                    "Extracted text length:",
                    len(extracted_text)
                    if extracted_text
                    else 0
                )

                print("First 200 characters:")

                print(
                    extracted_text[:200]
                    if extracted_text
                    else "NO TEXT"
                )

                status = "PROCESSED"

            except Exception as e:

                print("\n========================================")
                print("EXTRACTION FAILED")
                print("ERROR:", repr(e))
                print("========================================")

                extracted_text = None
                status = "FAILED"

        else:

            print("\n========================================")
            print("NO EXTRACTOR FOUND")
            print("========================================")

        # -----------------------------------------
        # 4. Create Document
        # -----------------------------------------

        document = Document(
            filename=file.filename,
            file_path=str(file_path),
            file_size=file_path.stat().st_size,
            content_type=file.content_type,
            extracted_text=extracted_text,
            status=status,
            workspace_id=workspace_id,
        )

        # -----------------------------------------
        # 5. Save Document
        # -----------------------------------------

        result = self.repository.create(
            db,
            document,
        )

        print("\nDOCUMENT SAVED")
        print("Document ID:", result.id)
        print("Status:", result.status)

        # -----------------------------------------
        # 6. Create chunks
        # -----------------------------------------

        if extracted_text and status == "PROCESSED":

            print("\n========================================")
            print("CREATING DOCUMENT CHUNKS")
            print("========================================")

            try:

                chunks = self.chunk_service.create_chunks(
                    db=db,
                    document_id=result.id,
                    extracted_text=extracted_text,
                    chunk_size=1000,
                    overlap=200,
                )

                print(
                    "CHUNKS CREATED:",
                    len(chunks)
                )

            except Exception as e:

                print("\n========================================")
                print("CHUNKING FAILED")
                print("ERROR:", repr(e))
                print("========================================")

        else:

            print(
                "\nSkipping chunking because no extracted text is available."
            )

        # -----------------------------------------
        # 7. Finished
        # -----------------------------------------

        print("\n========================================")
        print("DOCUMENT UPLOAD FINISHED")
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