from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.common.messages import UNIT_OF_WORK_NOT_STARTED
from app.db.base import UnitOfWorkABC
from app.repositories.user.base import UserRepositoryABC
from app.repositories.user.user import UserRepository


class SQLAlchemyUnitOfWork(UnitOfWorkABC):
    """*SQLAlchemy unit of work built on top of an async session factory.*

    The session is opened on entering the context and closed on leaving it,
    the changes are persisted only after an explicit `commit()`.

    Example:
        ```python
        async with SQLAlchemyUnitOfWork(async_session) as uow:
            user = await uow.users.add(email='employee@investlink.io')
            await uow.commit()
        ```
    """

    def __init__(self, session_factory: async_sessionmaker[AsyncSession]) -> None:
        self._session_factory = session_factory
        self._session: AsyncSession | None = None
        self._users: UserRepositoryABC | None = None

    @property
    def session(self) -> AsyncSession:
        """*Session shared by all repositories of the unit of work.*

        Returns:
            AsyncSession: the currently opened session.

        Raises:
            RuntimeError: if the unit of work has not been entered yet.
        """
        if self._session is None:
            raise RuntimeError(UNIT_OF_WORK_NOT_STARTED)

        return self._session

    @property
    def users(self) -> UserRepositoryABC:
        """*User repository bound to the session of the unit of work.*

        Returns:
            UserRepositoryABC: lazily created user repository.
        """
        if self._users is None:
            self._users = UserRepository(self.session)

        return self._users

    async def __aenter__(self) -> Self:
        """*Opens the session and makes the repositories available.*

        Returns:
            Self: the started unit of work.
        """
        self._session = self._session_factory()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """*Rolls back the uncommitted changes and closes the session.*"""
        session = self.session

        try:
            if exc_type is not None:
                await session.rollback()
        finally:
            await session.close()
            self._session = None
            self._users = None

    async def commit(self) -> None:
        """*Commits everything done inside the unit of work.*

        Raises:
            Exception: re-raises any error occurred during the commit after a rollback.
        """
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
            raise

    async def rollback(self) -> None:
        """*Discards everything done inside the unit of work.*"""
        await self.session.rollback()

    async def flush(self) -> None:
        """*Sends the pending changes to the database without committing them.*"""
        await self.session.flush()

    async def refresh(self, entity: object) -> None:
        """*Reloads the state of the given entity from the database.*"""
        await self.session.refresh(entity)
