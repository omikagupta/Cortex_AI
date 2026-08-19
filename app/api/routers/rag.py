from uuid import UUID

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.services.rag.rag_service import RAGService


router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


class RAGRequest(BaseModel):
    document_id: UUID
    question: str
    top_k: int = 2


@router.post("/ask")
def ask_question(
    request: RAGRequest,
    db: Session = Depends(get_db),
):
    rag_service = RAGService()

    return rag_service.ask(
        db=db,
        document_id=request.document_id,
        question=request.question,
        top_k=request.top_k,
    )