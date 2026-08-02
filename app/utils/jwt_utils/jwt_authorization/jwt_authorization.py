from typing import Any

from async_fastapi_jwt_auth import AuthJWT

from app.utils.jwt_utils.jwt_authorization.base import JWTAuthProviderABC


class JWTAuthProvider(AuthJWT, JWTAuthProviderABC):
    """*JWT authorization provider reading the claims of the current request token.*"""

    async def get_claims(self) -> Any:
        """*Returns the claims of the token attached to the current request.*

        Returns:
            Any: raw JWT claims.
        """
        return await self.get_raw_jwt()

    async def get_user_id(self) -> int:
        """*Extracts the authorized user identifier from the token subject.*

        Returns:
            int: user identifier.

        Raises:
            ValueError: if the subject is missing or is not a valid identifier.
        """
        claims = await self.get_claims()

        sub = claims['sub']

        if sub is None:
            raise ValueError()

        user_id = self._parse_user_id(sub)

        return user_id

    @staticmethod
    def _parse_user_id(sub: Any) -> int:
        """*Converts the token subject into a user identifier.*

        Returns:
            int: user identifier.

        Raises:
            ValueError: if the subject cannot be converted to an integer.
        """
        try:
            return int(sub)
        except (ValueError, TypeError):
            raise ValueError()
