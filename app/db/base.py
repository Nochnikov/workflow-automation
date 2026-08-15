from abc import ABC, abstractmethod
from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user.base import UserRepositoryABC


class UnitOfWorkABC(ABC):
    """*Contract of the unit of work: owns the session and the transaction boundary.*

    Repositories exposed by the unit of work share a single session,
    so every change made through them is committed or rolled back at once.
    """

    users: UserRepositoryABC

    @property
    @abstractmethod
    def session(self) -> AsyncSession:
        """*Session shared by all repositories of the unit of work.*

        Returns:
            AsyncSession: the currently opened session.

        Raises:
            NotImplementedError: if the subclass does not implement the property.
        """
        raise NotImplementedError()

    @abstractmethod
    async def __aenter__(self) -> Self:
        """*Opens the session and makes the repositories available.*

        Returns:
            Self: the started unit of work.

        Raises:
            NotImplementedError: if the subclass does not implement the method.
        """
        raise NotImplementedError()

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """*Rolls back the uncommitted changes and closes the session.*

        Raises:
            NotImplementedError: if the subclass does not implement the method.
        """
        raise NotImplementedError()

    @abstractmethod
    async def commit(self) -> None:
        """*Commits everything done inside the unit of work.*

        Raises:
            NotImplementedError: if the subclass does not implement the method.
        """
        raise NotImplementedError()

    @abstractmethod
    async def rollback(self) -> None:
        """*Discards everything done inside the unit of work.*

        Raises:
            NotImplementedError: if the subclass does not implement the method.
        """
        raise NotImplementedError()

    @abstractmethod
    async def flush(self) -> None:
        """*Sends the pending changes to the database without committing them.*

        Raises:
            NotImplementedError: if the subclass does not implement the method.
        """
        raise NotImplementedError()

    @abstractmethod
    async def refresh(self, entity: object) -> None:
        """*Reloads the state of the given entity from the database.*

        Raises:
            NotImplementedError: if the subclass does not implement the method.
        """
        raise NotImplementedError()
