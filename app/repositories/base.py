from typing import Generic, TypeVar

from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Base repository responsible ONLY for database operations.

    NOTE:
    This class NEVER commits transactions.
    Transaction management belongs to the Service layer.
    """

    def __init__(self, db: Session, model: type[ModelType]):
        self.db = db
        self.model = model

    def create(self, obj: ModelType) -> ModelType:
        self.db.add(obj)
        self.db.flush()
        self.db.refresh(obj)
        return obj

    def get_by_id(self, obj_id: int) -> ModelType | None:
        return (
            self.db.query(self.model)
            .filter(self.model.id == obj_id)
            .first()
        )

    def get_all(self) -> list[ModelType]:
        return self.db.query(self.model).all()

    def update(self, obj: ModelType) -> ModelType:
        self.db.flush()
        self.db.refresh(obj)
        return obj

    def delete(self, obj: ModelType) -> None:
        self.db.delete(obj)
        self.db.flush()

    def exists(self, obj_id: int) -> bool:
        return (
            self.db.query(self.model)
            .filter(self.model.id == obj_id)
            .first()
            is not None
        )