from typing import Generic, TypeVar

from sqlalchemy.exc import SQLAlchemyError

from app.repositories.base import BaseRepository

ModelType = TypeVar("ModelType")


class BaseService(Generic[ModelType]):
    """
    Base service responsible for business logic
    and transaction management.
    """

    def __init__(self, repository: BaseRepository[ModelType]):
        self.repository = repository

    @property
    def db(self):
        return self.repository.db

    def create(self, obj: ModelType) -> ModelType:
        try:
            entity = self.repository.create(obj)
            self.db.commit()
            return entity

        except SQLAlchemyError:
            self.db.rollback()
            raise

    def get_by_id(self, obj_id: int) -> ModelType | None:
        return self.repository.get_by_id(obj_id)

    def get_all(self) -> list[ModelType]:
        return self.repository.get_all()

    def update(self, obj: ModelType) -> ModelType:
        try:
            entity = self.repository.update(obj)
            self.db.commit()
            return entity

        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete(self, obj: ModelType) -> None:
        try:
            self.repository.delete(obj)
            self.db.commit()

        except SQLAlchemyError:
            self.db.rollback()
            raise

    def exists(self, obj_id: int) -> bool:
        return self.repository.exists(obj_id)

    def commit(self) -> None:
        """
        Allows child services to commit manually
        after multiple repository operations.
        """
        self.db.commit()

    def rollback(self) -> None:
        """
        Rolls back the current transaction.
        """
        self.db.rollback()