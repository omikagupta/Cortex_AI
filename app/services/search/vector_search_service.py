import json
import math
import re

from sqlalchemy.orm import Session

from app.models import DocumentChunk
from app.services.embeddings.embedding_service import EmbeddingService


class VectorSearchService:

    def __init__(self):
        self.embedding_service = EmbeddingService()

    # -----------------------------------------
    # COSINE SIMILARITY
    # -----------------------------------------

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

    # -----------------------------------------
    # KEYWORD SCORE
    # -----------------------------------------

    def keyword_score(
        self,
        query: str,
        content: str,
    ) -> float:

        stop_words = {
            "what",
            "were",
            "was",
            "are",
            "is",
            "the",
            "a",
            "an",
            "to",
            "of",
            "in",
            "on",
            "for",
            "and",
            "or",
            "used",
            "how",
            "why",
            "when",
            "where",
            "which",
            "who",
            "does",
            "do",
            "did",
            "can",
            "could",
            "would",
            "should",
        }

        query = query.lower()
        content = content.lower()

        query_words = re.findall(
            r"\b[a-zA-Z0-9]+\b",
            query,
        )

        content_words = re.findall(
            r"\b[a-zA-Z0-9]+\b",
            content,
        )

        query_words = [
            word
            for word in query_words
            if word not in stop_words
        ]

        if not query_words:
            return 0.0

        content_word_set = set(content_words)

        matched_words = sum(
            1
            for word in query_words
            if word in content_word_set
        )

        score = matched_words / len(query_words)

        # -----------------------------------------
        # IMPORTANT TERM BONUS
        # -----------------------------------------

        important_terms = {
            "sensor",
            "sensors",
            "stress",
            "ppg",
            "hrv",
            "eda",
            "gsr",
            "temperature",
            "accelerometer",
            "heart",
            "rate",
        }

        important_matches = sum(
            1
            for word in query_words
            if word in important_terms
            and word in content_word_set
        )

        if important_matches > 0:
            score += 0.15 * important_matches

        return min(score, 1.0)

    # -----------------------------------------
    # RELEVANCE SCORE
    # -----------------------------------------

    def relevance_score(
        self,
        query: str,
        content: str,
    ) -> float:

        query_lower = query.lower()
        content_lower = content.lower()

        score = 0.0

        # -----------------------------------------
        # EXACT PHRASE MATCH
        # -----------------------------------------

        if query_lower in content_lower:
            score += 0.5

        # -----------------------------------------
        # SENSOR-RELATED TERMS
        # -----------------------------------------

        sensor_terms = [
            "sensor",
            "sensors",
            "ppg",
            "hrv",
            "eda",
            "gsr",
            "skin temperature",
            "accelerometer",
            "heart rate",
        ]

        matched_sensor_terms = 0

        for term in sensor_terms:
            if term in content_lower:
                matched_sensor_terms += 1

        if matched_sensor_terms > 0:
            score += min(
                0.1 * matched_sensor_terms,
                0.5,
            )

        return min(score, 1.0)

    # -----------------------------------------
    # HYBRID SEARCH
    # -----------------------------------------

    def search(
        self,
        db: Session,
        document_id,
        query: str,
        top_k: int = 5,
    ):

        # -----------------------------------------
        # 1. Generate query embedding
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

            # -----------------------------------------
            # Semantic similarity
            # -----------------------------------------

            semantic_score = self.cosine_similarity(
                query_embedding,
                chunk_embedding,
            )

            # -----------------------------------------
            # Keyword similarity
            # -----------------------------------------

            keyword_score = self.keyword_score(
                query,
                chunk.content,
            )

            # -----------------------------------------
            # Entity / phrase relevance
            # -----------------------------------------

            relevance_score = self.relevance_score(
                query,
                chunk.content,
            )

            # -----------------------------------------
            # HYBRID SCORE
            # -----------------------------------------
            #
            # 60% semantic
            # 25% keyword
            # 15% relevance
            #
            # Semantic search finds meaning.
            # Keyword search finds exact terms.
            # Relevance search boosts important
            # phrases and sensor-related content.
            # -----------------------------------------

            final_score = (
                0.50 * semantic_score
                + 0.35 * keyword_score
                + 0.15 * relevance_score
            )

            results.append(
                {
                    "chunk_id": chunk.id,
                    "chunk_index": chunk.chunk_index,
                    "content": chunk.content,
                    "similarity": final_score,
                    "semantic_score": semantic_score,
                    "keyword_score": keyword_score,
                    "relevance_score": relevance_score,
                }
            )

        # -----------------------------------------
        # 4. Sort by final score
        # -----------------------------------------

        results.sort(
            key=lambda x: x["similarity"],
            reverse=True,
        )

        # -----------------------------------------
        # 5. Return top K
        # -----------------------------------------

        return results[:top_k]