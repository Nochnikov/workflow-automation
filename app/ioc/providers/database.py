from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import UnitOfWorkABC
from app.db.postgres import async_session
from app.db.uow import SQLAlchemyUnitOfWork


class DatabaseProvider(Provider):
    """*DI provider of the database session and the unit of work built on top of it.*"""

    @provide(scope=Scope.REQUEST)
    async def session(self) -> AsyncIterator[AsyncSession]:
        """*Opens a session living as long as the current request.*

        Yields:
            AsyncSession: session closed once the request is handled.
        """
        async with async_session() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def uow(
        self,
        session: AsyncSession,
    ) -> UnitOfWorkABC:
        """*Builds the unit of work sharing the session of the current request.*

        Returns:
            UnitOfWorkABC: unit of work whose repositories work in that session.
        """
        return SQLAlchemyUnitOfWork(session)
