from abc import ABC, abstractmethod

from app.models.users import User
from app.repositories.base import RepositoryABC


class UserRepositoryABC(RepositoryABC[User], ABC):
    """*Contract of the user repository.*"""

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        """*Returns the user registered with the given email address.*

        Returns:
            User | None: the user or `None` if nobody uses this email.

        Raises:
            NotImplementedError: if the subclass does not implement the method.
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_by_phone_number(self, phone_number: str) -> User | None:
        """*Returns the user registered with the given phone number.*

        Returns:
            User | None: the user or `None` if nobody uses this phone number.

        Raises:
            NotImplementedError: if the subclass does not implement the method.
        """
        raise NotImplementedError()
