from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from app.db.base import UnitOfWorkABC
from app.db.postgres import async_session, engine
from app.db.uow import SQLAlchemyUnitOfWork


class DatabaseProvider(Provider):
    """*DI provider of the database engine, the session factory and the unit of work.*"""

    @provide(scope=Scope.APP)
    async def db_engine(self) -> AsyncIterator[AsyncEngine]:
        """*Provides the application engine and disposes its pool on shutdown.*

        Yields:
            AsyncEngine: engine shared by the whole application.
        """
        yield engine
        await engine.dispose()

    @provide(scope=Scope.APP)
    def session_factory(self, db_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        """*Provides the session factory bound to the application engine.*

        Returns:
            async_sessionmaker[AsyncSession]: factory of async sessions.
        """
        return async_session

    @provide(scope=Scope.REQUEST)
    async def unit_of_work(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> AsyncIterator[UnitOfWorkABC]:
        """*Provides a unit of work living as long as the current request.*

        Yields:
            UnitOfWorkABC: started unit of work closed once the request is handled.
        """
        async with SQLAlchemyUnitOfWork(session_factory) as uow:
            yield uow
