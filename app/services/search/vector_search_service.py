import json
import math

from sqlalchemy.orm import Session

from app.models import DocumentChunk
from app.services.embeddings.embedding_service import EmbeddingService


class VectorSearchService:

    def __init__(self):
        self.embedding_service = EmbeddingService()

    def cosine_similarity(
        self,
        vector_a: list[float],
        vector_b: list[float],
    ) -> float:

        if len(vector_a) != len(vector_b):
            raise ValueError(
                "Vectors must have the same dimension"
            )

        dot_product = sum(
            a * b
            for a, b in zip(vector_a, vector_b)
        )

        magnitude_a = math.sqrt(
            sum(a * a for a in vector_a)
        )

        magnitude_b = math.sqrt(
            sum(b * b for b in vector_b)
        )

        if magnitude_a == 0 or magnitude_b == 0:
            return 0.0

        return dot_product / (
            magnitude_a * magnitude_b
        )

    def search(
        self,
        db: Session,
        document_id,
        query: str,
        top_k: int = 5,
    ):

        # -----------------------------------------
        # 1. Generate embedding for query
        # -----------------------------------------

        query_embedding = (
            self.embedding_service.create_embedding(
                query
            )
        )

        # -----------------------------------------
        # 2. Get document chunks
        # -----------------------------------------

        chunks = (
            db.query(DocumentChunk)
            .filter(
                DocumentChunk.document_id
                == document_id
            )
            .all()
        )

        results = []

        # -----------------------------------------
        # 3. Compare query with every chunk
        # -----------------------------------------

        for chunk in chunks:

            if not chunk.embedding:
                continue

            chunk_embedding = json.loads(
                chunk.embedding
            )

            similarity = self.cosine_similarity(
                query_embedding,
                chunk_embedding,
            )

            results.append(
                {
                    "chunk_id": chunk.id,
                    "chunk_index": chunk.chunk_index,
                    "content": chunk.content,
                    "similarity": similarity,
                }
            )

        # -----------------------------------------
        # 4. Sort by similarity
        # -----------------------------------------

        results.sort(
            key=lambda x: x["similarity"],
            reverse=True,
        )

        # -----------------------------------------
        # 5. Return top K
        # -----------------------------------------

        return results[:top_k]