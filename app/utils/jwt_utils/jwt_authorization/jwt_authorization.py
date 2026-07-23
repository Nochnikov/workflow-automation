from typing import Any

from async_fastapi_jwt_auth import AuthJWT

from app.utils.jwt_utils.jwt_authorization.base import JWTAuthProviderABC


class JWTAuthProvider(AuthJWT, JWTAuthProviderABC):
    async def get_claims(self) -> Any:
        return await self.get_raw_jwt()

    async def get_user_id(self) -> int:
        claims = await self.get_claims()

        sub = claims['sub']

        if sub is None:
            raise ValueError()

        user_id = self._parse_user_id(sub)

        return user_id

    @staticmethod
    def _parse_user_id(sub: Any) -> int:
        try:
            return int(sub)
        except (ValueError, TypeError):
            raise ValueError()
