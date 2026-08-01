from typing import Generic, TypeVar

from app.repositories.base import BaseRepository

ModelType = TypeVar("ModelType")


class BaseService(Generic[ModelType]):
    """
    Base service responsible for coordinating business logic.
    """

    def __init__(self, repository: BaseRepository[ModelType]):
        self.repository = repository

    def create(self, obj: ModelType) -> ModelType:
        """
        Create a new entity.
        """
        return self.repository.create(obj)

    def get_by_id(self, obj_id: int) -> ModelType | None:
        """
        Retrieve an entity by its ID.
        """
        return self.repository.get_by_id(obj_id)

    def get_all(self) -> list[ModelType]:
        """
        Retrieve all entities.
        """
        return self.repository.get_all()

    def update(self, obj: ModelType) -> ModelType:
        """
        Update an existing entity.
        """
        return self.repository.update(obj)

    def delete(self, obj: ModelType) -> None:
        """
        Delete an entity.
        """
        self.repository.delete(obj)

    def exists(self, obj_id: int) -> bool:
        """
        Check whether an entity exists.
        """
        return self.repository.exists(obj_id)