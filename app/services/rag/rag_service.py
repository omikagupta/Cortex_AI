from google import genai

from app.core.config import settings
from app.services.search.vector_search_service import VectorSearchService
from app.services.rag.rag_context_builder import RAGContextBuilder


class RAGService:

    def __init__(self):
        self.vector_search = VectorSearchService()
        self.context_builder = RAGContextBuilder()

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = "gemini-3.6-flash"

        # Minimum similarity required before
        # sending the retrieved context to Gemini.
        self.relevance_threshold = 0.45

    def ask(
        self,
        db,
        document_id,
        question: str,
        top_k: int = 5,
    ):

        # -----------------------------------------
        # 1. Retrieve relevant chunks
        # -----------------------------------------

        search_results = self.vector_search.search(
            db,
            document_id,
            question,
            top_k,
        )

        # -----------------------------------------
        # 2. Handle no search results
        # -----------------------------------------

        if not search_results:
            return {
                "question": question,
                "answer": "I could not find the answer in the document.",
                "sources": [],
            }

        # -----------------------------------------
        # 3. Check relevance
        # -----------------------------------------

        relevant_results = [
            result
            for result in search_results
            if result["similarity"] >= self.relevance_threshold
        ]

        # -----------------------------------------
        # 4. If nothing is relevant
        # -----------------------------------------

        if not relevant_results:
            return {
                "question": question,
                "answer": "I could not find the answer in the document.",
                "sources": [],
            }

        # -----------------------------------------
        # 5. Build context
        # -----------------------------------------

        context = self.context_builder.build_context(
            relevant_results
        )

        # -----------------------------------------
        # 6. Create grounded prompt
        # -----------------------------------------

        prompt = f"""
You are an AI assistant answering questions
about a document.

Answer the user's question ONLY using the
information contained in the document context.

STRICT RULES:

1. Do not use outside knowledge.
2. Do not invent information.
3. Do not make assumptions that are not supported
   by the document.
4. If the answer cannot be found in the context,
   say exactly:

"I could not find the answer in the document."

5. Answer clearly and directly.
6. You may combine information from multiple
   relevant sections of the document.
7. Do not mention chunk numbers.
8. Do not mention relevance scores.
9. Do not mention embeddings.
10. Do not mention vector search.
11. Do not mention the RAG system.
12. If the question asks for a list, use bullet points.
13. If the question asks for a number, state it clearly.

DOCUMENT CONTEXT:

{context}

USER QUESTION:

{question}

ANSWER:
"""

        # -----------------------------------------
        # 7. Generate answer
        # -----------------------------------------

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        # -----------------------------------------
        # 8. Build source information
        # -----------------------------------------

        sources = []

        for result in relevant_results:

            sources.append(
                {
                    "chunk_index": result["chunk_index"],
                    "content": result["content"],
                    "score": result["similarity"],
                }
            )

        # -----------------------------------------
        # 9. Return structured response
        # -----------------------------------------

        return {
            "question": question,
            "answer": response.text,
            "sources": sources,
        }