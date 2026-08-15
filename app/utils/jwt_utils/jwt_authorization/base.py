from abc import ABC, abstractmethod
from typing import Any


class JWTAuthProviderABC(ABC):
    """*Contract of the JWT authorization provider.*"""

    @abstractmethod
    async def get_claims(self) -> Any:
        """*Returns the claims of the token attached to the current request.*

        Returns:
            Any: raw JWT claims.

        Raises:
            NotImplementedError: if the subclass does not implement the method.
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_user_id(self) -> int:
        """*Returns the identifier of the authorized user.*

        Returns:
            int: user identifier.

        Raises:
            NotImplementedError: if the subclass does not implement the method.
        """
        raise NotImplementedError()
