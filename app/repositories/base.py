from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any

from app.db.postgres import Base


class RepositoryABC[ModelT: Base](ABC):
    """*Contract of a data access repository of a single ORM model.*"""

    @abstractmethod
    async def add(self, **values: Any) -> ModelT:
        """*Creates a new entity and flushes it to get the generated values.*

        Returns:
            ModelT: the persisted entity.

        Raises:
            NotImplementedError: if the subclass does not implement the method.
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_by_id(self, entity_id: int) -> ModelT | None:
        """*Returns the entity with the given identifier.*

        Returns:
            ModelT | None: the entity or `None` if it does not exist.

        Raises:
            NotImplementedError: if the subclass does not implement the method.
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_one(self, **filters: Any) -> ModelT | None:
        """*Returns a single entity matching the given field filters.*

        Returns:
            ModelT | None: the entity or `None` if nothing matches.

        Raises:
            NotImplementedError: if the subclass does not implement the method.
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_many(
        self,
        limit: int | None = None,
        offset: int | None = None,
        **filters: Any,
    ) -> Sequence[ModelT]:
        """*Returns all entities matching the given field filters.*

        Returns:
            Sequence[ModelT]: matching entities, possibly empty.

        Raises:
            NotImplementedError: if the subclass does not implement the method.
        """
        raise NotImplementedError()

    @abstractmethod
    async def update_by_id(self, entity_id: int, **values: Any) -> ModelT | None:
        """*Updates the entity with the given identifier.*

        Returns:
            ModelT | None: the updated entity or `None` if it does not exist.

        Raises:
            NotImplementedError: if the subclass does not implement the method.
        """
        raise NotImplementedError()

    @abstractmethod
    async def delete_by_id(self, entity_id: int) -> bool:
        """*Deletes the entity with the given identifier.*

        Returns:
            bool: `True` if a row was deleted.

        Raises:
            NotImplementedError: if the subclass does not implement the method.
        """
        raise NotImplementedError()

    @abstractmethod
    async def exists(self, **filters: Any) -> bool:
        """*Checks whether at least one entity matches the given field filters.*

        Returns:
            bool: `True` if a matching entity exists.

        Raises:
            NotImplementedError: if the subclass does not implement the method.
        """
        raise NotImplementedError()
