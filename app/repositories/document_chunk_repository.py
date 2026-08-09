from sqlalchemy.orm import Session

from app.models import DocumentChunk


class DocumentChunkRepository:

    def create(
        self,
        db: Session,
        chunk: DocumentChunk,
    ) -> DocumentChunk:

        db.add(chunk)
        db.commit()
        db.refresh(chunk)

        return chunk

    def create_many(
        self,
        db: Session,
        chunks: list[DocumentChunk],
    ) -> list[DocumentChunk]:

        db.add_all(chunks)
        db.commit()

        for chunk in chunks:
            db.refresh(chunk)

        return chunks

    def get_by_document(
        self,
        db: Session,
        document_id,
    ):

        return (
            db.query(DocumentChunk)
            .filter(
                DocumentChunk.document_id == document_id
            )
            .order_by(
                DocumentChunk.chunk_index
            )
            .all()
        )

    def delete_by_document(
        self,
        db: Session,
        document_id,
    ):

        (
            db.query(DocumentChunk)
            .filter(
                DocumentChunk.document_id == document_id
            )
            .delete(
                synchronize_session=False
            )
        )

        db.commit()