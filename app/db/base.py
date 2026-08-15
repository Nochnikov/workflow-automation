from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.users import UsersRepository


class UnitOfWorkABC(ABC):
    """*Contract of the unit of work: owns the session and the transaction boundary.*

    All the repositories it exposes share a single session, so every change
    made through them is committed or rolled back at once.
    """

    session: AsyncSession
    user_repository: UsersRepository

    @abstractmethod
    def transaction(self) -> AbstractAsyncContextManager[None]:
        """*Opens a transaction committed on a normal exit and rolled back on an error.*

        Returns:
            AbstractAsyncContextManager[None]: context manager of the transaction.

        Raises:
            NotImplementedError: if the subclass does not implement the method.
        """
        raise NotImplementedError()
