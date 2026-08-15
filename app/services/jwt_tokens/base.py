from abc import ABC, abstractmethod


class JWTHandlerABC(ABC):
    """*Contract of the JWT token handler.*"""

    @abstractmethod
    def create_access_token(self, user_id: int, claims: dict) -> tuple[str, str]:
        """*Issues an access token for the given user.*

        Returns:
            tuple[str, str]: encoded token and its jti.

        Raises:
            NotImplementedError: if the subclass does not implement the method.
        """
        raise NotImplementedError()

    @abstractmethod
    def create_refresh_token(self, user_id: int, access_jti: str) -> tuple[str, str]:
        """*Issues a refresh token bound to the given access token.*

        Returns:
            tuple[str, str]: encoded token and its jti.

        Raises:
            NotImplementedError: if the subclass does not implement the method.
        """
        raise NotImplementedError()
