from app.services.search.vector_search_service import VectorSearchService
from app.services.rag.rag_context_builder import RAGContextBuilder
from app.core.config import settings
from google import genai


class RAGService:

    def __init__(self):
        self.vector_search = VectorSearchService()
        self.context_builder = RAGContextBuilder()

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model = "gemini-3.6-flash"

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
        # 2. Build context
        # -----------------------------------------

        context = self.context_builder.build_context(
            search_results
        )

        # -----------------------------------------
        # 3. Create prompt
        # -----------------------------------------

        prompt = f"""
You are an AI assistant answering questions
about a document.

Answer the user's question ONLY using the
provided document context.

If the answer cannot be found in the context,
say:

"I could not find the answer in the document."

Do not invent information.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}

ANSWER:
"""

        # -----------------------------------------
        # 4. Ask Gemini
        # -----------------------------------------

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        # -----------------------------------------
        # 5. Return result
        # -----------------------------------------

        return {
            "question": question,
            "answer": response.text,
            "sources": search_results,
        }