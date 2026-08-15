from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres import Base


class BaseRepository[ModelType: Base](ABC):
    """*Contract of a data access repository of a single ORM model.*"""

    @abstractmethod
    async def create(self, *args: Any, **kwargs: Any) -> ModelType:
        """*Creates a new entity and flushes it to get the generated values.*

        Returns:
            ModelType: the persisted entity.

        Raises:
            NotImplementedError: if the subclass does not implement the method.
        """
        raise NotImplementedError()

    @abstractmethod
    async def update(self, *args: Any, **kwargs: Any) -> ModelType:
        """*Updates the entity with the given identifier.*

        Returns:
            ModelType: the updated entity.

        Raises:
            NotImplementedError: if the subclass does not implement the method.
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_by_field(self, *args: Any, **kwargs: Any) -> ModelType:
        """*Returns a single entity matching the given field filters.*

        Returns:
            ModelType: the matching entity.

        Raises:
            NotImplementedError: if the subclass does not implement the method.
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_multi(self, *args: Any, **kwargs: Any) -> list[ModelType]:
        """*Returns all entities matching the given field filters.*

        Returns:
            list[ModelType]: matching entities, possibly empty.

        Raises:
            NotImplementedError: if the subclass does not implement the method.
        """
        raise NotImplementedError()


class Repository[
    ModelType: Base,
    CreateSchemaType: BaseModel,
    UpdateSchemaType: BaseModel,
](BaseRepository[ModelType]):
    """*SQLAlchemy repository working in the session owned by the unit of work.*

    The repository never commits: the transaction boundary belongs to the unit of work,
    so every change stays pending until `UnitOfWorkABC.transaction()` closes it.
    """

    def __init__(self, model: type[ModelType], db: AsyncSession):
        self._model = model
        self._db = db

    async def create(self, data: CreateSchemaType) -> ModelType:
        """*Creates a new entity from the schema and flushes it to get the generated values.*

        Returns:
            ModelType: the persisted entity, already filled with its identifier.
        """
        entity = self._model(**data.model_dump(exclude_unset=True))

        self._db.add(entity)
        await self._db.flush()

        return entity

    async def update(self, entity_id: int, data: UpdateSchemaType) -> ModelType | None:
        """*Applies the fields set in the schema to the entity with the given identifier.*

        Returns:
            ModelType | None: the updated entity or `None` if it does not exist.
        """
        entity = await self.get_by_field(id=entity_id)

        if entity is None:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(entity, field, value)

        await self._db.flush()

        return entity

    async def get_by_field(self, **filters: Any) -> ModelType | None:
        """*Returns a single entity matching the given field filters.*

        Returns:
            ModelType | None: the entity or `None` if nothing matches.
        """
        result = await self._db.execute(select(self._model).filter_by(**filters))

        return result.scalars().first()

    async def get_multi(
        self,
        limit: int | None = None,
        offset: int | None = None,
        **filters: Any,
    ) -> list[ModelType]:
        """*Returns all entities matching the given field filters.*

        Returns:
            list[ModelType]: matching entities, possibly empty.
        """
        stmt = select(self._model).filter_by(**filters)

        if offset is not None:
            stmt = stmt.offset(offset)

        if limit is not None:
            stmt = stmt.limit(limit)

        result = await self._db.execute(stmt)

        return list(result.scalars().all())

    async def delete(self, entity_id: int) -> bool:
        """*Deletes the entity with the given identifier.*

        Returns:
            bool: `True` if a row was deleted.
        """
        result = await self._db.execute(delete(self._model).filter_by(id=entity_id))

        return bool(result.rowcount)

    async def exists(self, **filters: Any) -> bool:
        """*Checks whether at least one entity matches the given field filters.*

        Returns:
            bool: `True` if a matching entity exists.
        """
        result = await self._db.execute(select(select(self._model).filter_by(**filters).exists()))

        return bool(result.scalar())
