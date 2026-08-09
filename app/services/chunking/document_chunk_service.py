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

        print("\n========================================")
        print("DOCUMENT CHUNKING STARTED")
        print("========================================")

        # -----------------------------------------
        # 1. Create text chunks
        # -----------------------------------------

        chunks = chunk_text(
            text,
            chunk_size,
            overlap,
        )

        print("Document ID:", document_id)
        print("Total chunks:", len(chunks))

        created_chunks = []

        # -----------------------------------------
        # 2. Process chunks
        # -----------------------------------------

        for index, content in enumerate(chunks):

            print("\n----------------------------------------")
            print("Processing chunk:", index)
            print("Content length:", len(content))

            # -------------------------------------
            # Generate Gemini embedding
            # -------------------------------------

            embedding = self.embedding_service.create_embedding(
                content
            )

            print(
                "Embedding dimension:",
                len(embedding)
            )

            # -------------------------------------
            # Convert embedding to JSON string
            # -------------------------------------

            import json

            embedding_string = json.dumps(embedding)

            # -------------------------------------
            # Create DocumentChunk object
            # -------------------------------------

            chunk = DocumentChunk(
                document_id=document_id,
                chunk_index=index,
                content=content,
                embedding=embedding_string,
            )

            # -------------------------------------
            # Save chunk
            # -------------------------------------

            saved_chunk = self.repository.create(
                db,
                chunk,
            )

            created_chunks.append(saved_chunk)

            print(
                "Chunk saved:",
                saved_chunk.id
            )

        print("\n========================================")
        print("DOCUMENT CHUNKING COMPLETED")
        print("Created chunks:", len(created_chunks))
        print("========================================")

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