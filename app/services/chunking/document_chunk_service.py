from sqlalchemy.orm import Session

from app.models import DocumentChunk
from app.repositories.document_chunk_repository import DocumentChunkRepository
from app.services.chunking.text_chunker import chunk_text
from app.services.embeddings.embedding_service import EmbeddingService


class DocumentChunkService:

    def __init__(self):

        self.repository = DocumentChunkRepository()

        self.embedding_service = EmbeddingService()

    def create_chunks(
        self,
        db: Session,
        document_id,
        text: str,
        chunk_size: int = 1000,
        overlap: int = 200,
    ):

        if not text or not text.strip():
            raise ValueError(
                "Cannot create chunks from empty text"
            )

        print("\n========================================")
        print("DOCUMENT CHUNKING STARTED")
        print("========================================")

        chunks = chunk_text(
            text,
            chunk_size,
            overlap,
        )

        print(
            "Document ID:",
            document_id,
        )

        print(
            "Total chunks:",
            len(chunks),
        )

        if not chunks:
            raise ValueError(
                "Text chunking produced zero chunks"
            )

        created_chunks = []

        for index, content in enumerate(chunks):

            print("\n----------------------------------------")
            print("Processing chunk:", index)
            print("Content length:", len(content))

            # =====================================
            # Generate embedding
            # =====================================

            print("Generating Gemini embedding...")

            embedding = (
                self.embedding_service.create_embedding(
                    content
                )
            )

            if not embedding:
                raise ValueError(
                    f"Empty embedding returned for chunk {index}"
                )

            print(
                "Embedding dimension:",
                len(embedding),
            )

            # =====================================
            # Save chunk
            # =====================================

            import json

            embedding_string = json.dumps(
                embedding
            )

            chunk = DocumentChunk(
                document_id=document_id,
                chunk_index=index,
                content=content,
                embedding=embedding_string,
            )

            saved_chunk = self.repository.create(
                db,
                chunk,
            )

            created_chunks.append(
                saved_chunk
            )

            print(
                "Chunk saved:",
                saved_chunk.id,
            )

        print("\n========================================")
        print("DOCUMENT CHUNKING COMPLETED")
        print("========================================")

        print(
            "Created chunks:",
            len(created_chunks),
        )

        print("========================================\n")

        return created_chunks

    def get_chunks(
        self,
        db: Session,
        document_id,
    ):

        return self.repository.get_by_document(
            db,
            document_id,
        )

    def delete_chunks(
        self,
        db: Session,
        document_id,
    ):

        self.repository.delete_by_document(
            db,
            document_id,
        )