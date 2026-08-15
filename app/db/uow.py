from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import UnitOfWorkABC
from app.models import User
from app.repositories.users import UsersRepository


class SQLAlchemyUnitOfWork(UnitOfWorkABC):
    """*SQLAlchemy unit of work sharing one session between all its repositories.*

    The changes are persisted only when the `transaction()` block is left without an error.

    Example:
        ```python
        async with uow.transaction():
            user = await uow.user_repository.create(data)
        ```
    """

    def __init__(self, session: AsyncSession):
        self.__init_repositories(session)

    def __init_repositories(self, session: AsyncSession) -> None:
        """*Binds the session and builds the repositories working on top of it.*"""
        self.session = session
        self.user_repository = UsersRepository(User, self.session)

    @asynccontextmanager
    async def transaction(self) -> AsyncGenerator[None, None]:
        """*Opens a transaction committed on leaving the block and rolled back on an error.*

        The integrity violations are swallowed: the transaction is rolled back
        and the control returns to the caller without an exception.

        Yields:
            None: control back to the caller for the duration of the transaction.

        Raises:
            Exception: re-raises any error except `IntegrityError` after a rollback.
        """
        try:
            async with self.session.begin():
                yield
        except IntegrityError:
            pass
