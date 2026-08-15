from collections.abc import Sequence
from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.postgres import Base
from app.repositories.base import RepositoryABC


class SQLAlchemyRepository[ModelT: Base](RepositoryABC[ModelT]):
    """*SQLAlchemy repository operating inside the session owned by the unit of work.*

    Subclasses only have to bind the `model` attribute to a concrete ORM model.
    The repository never commits: transaction boundaries belong to the unit of work.
    """

    model: type[ModelT]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @property
    def session(self) -> AsyncSession:
        """*Session the repository is bound to.*

        Returns:
            AsyncSession: session shared with the owning unit of work.
        """
        return self._session

    async def add(self, **values: Any) -> ModelT:
        """*Creates a new entity and flushes it to get the generated values.*

        Returns:
            ModelT: the persisted entity.
        """
        entity = self.model(**values)
        self._session.add(entity)
        await self._session.flush()
        return entity

    async def get_by_id(self, entity_id: int) -> ModelT | None:
        """*Returns the entity with the given identifier.*

        Returns:
            ModelT | None: the entity or `None` if it does not exist.
        """
        return await self._session.get(self.model, entity_id)

    async def get_one(self, **filters: Any) -> ModelT | None:
        """*Returns a single entity matching the given field filters.*

        Returns:
            ModelT | None: the entity or `None` if nothing matches.
        """
        result = await self._session.execute(select(self.model).filter_by(**filters))
        return result.scalars().first()

    async def get_many(
        self,
        limit: int | None = None,
        offset: int | None = None,
        **filters: Any,
    ) -> Sequence[ModelT]:
        """*Returns all entities matching the given field filters.*

        Returns:
            Sequence[ModelT]: matching entities, possibly empty.
        """
        stmt = select(self.model).filter_by(**filters)

        if offset is not None:
            stmt = stmt.offset(offset)

        if limit is not None:
            stmt = stmt.limit(limit)

        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def update_by_id(self, entity_id: int, **values: Any) -> ModelT | None:
        """*Updates the entity with the given identifier.*

        Returns:
            ModelT | None: the updated entity or `None` if it does not exist.
        """
        entity = await self.get_by_id(entity_id)

        if entity is None:
            return None

        for field, value in values.items():
            setattr(entity, field, value)

        await self._session.flush()
        return entity

    async def delete_by_id(self, entity_id: int) -> bool:
        """*Deletes the entity with the given identifier.*

        Returns:
            bool: `True` if a row was deleted.
        """
        result = await self._session.execute(delete(self.model).filter_by(id=entity_id))
        return bool(result.rowcount)

    async def exists(self, **filters: Any) -> bool:
        """*Checks whether at least one entity matches the given field filters.*

        Returns:
            bool: `True` if a matching entity exists.
        """
        stmt = select(select(self.model).filter_by(**filters).exists())
        result = await self._session.execute(stmt)
        return bool(result.scalar())
