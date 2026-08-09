from sqlalchemy.orm import Session

from app.repositories import DocumentChunkRepository
from app.services.embeddings.embedding_service import EmbeddingService


class SemanticSearchService:

    def __init__(self):
        self.repository = DocumentChunkRepository()
        self.embedding_service = EmbeddingService()

    def search(
        self,
        db: Session,
        workspace_id,
        query: str,
        top_k: int = 5,
    ):
        # -----------------------------------------
        # 1. Generate embedding for query
        # -----------------------------------------

        query_embedding = self.embedding_service.generate_embedding(
            query
        )

        # -----------------------------------------
        # 2. Search similar chunks
        # -----------------------------------------

        results = self.repository.search_similar(
            db=db,
            workspace_id=workspace_id,
            embedding=query_embedding,
            top_k=top_k,
        )

        return results