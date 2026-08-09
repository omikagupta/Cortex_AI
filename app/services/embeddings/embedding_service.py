from google import genai

from app.core.config import settings


class EmbeddingService:

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = "gemini-embedding-001"

    def create_embedding(self, text: str) -> list[float]:

        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        response = self.client.models.embed_content(
            model=self.model,
            contents=text,
        )

        return response.embeddings[0].values

    def create_embeddings(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        if not texts:
            return []

        embeddings = []

        for text in texts:

            if not text or not text.strip():
                embeddings.append([])
                continue

            response = self.client.models.embed_content(
                model=self.model,
                contents=text,
            )

            embeddings.append(
                response.embeddings[0].values
            )

        return embeddings