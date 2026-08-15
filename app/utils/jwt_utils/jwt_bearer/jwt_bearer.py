import http
from typing import Any

import Redis
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.common import messages
from app.utils.security import decode_token


class JWTBearer(HTTPBearer):
    """*Bearer security dependency validating a JWT token against the Redis blacklist.*"""

    def __init__(self, auto_error: bool = True):
        """*Configures the underlying bearer scheme.*"""
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict[str, Any]:
        """*Validates the request bearer token and returns its decoded payload.*

        Returns:
            dict[str, Any]: decoded token payload.

        Raises:
            HTTPException: if the credentials are missing, the scheme is not bearer,
                the token is invalid, blacklisted or absent in Redis.
        """
        credentials: HTTPAuthorizationCredentials | None = await super().__call__(request)
        if not credentials:
            raise HTTPException(
                status_code=http.HTTPStatus.FORBIDDEN,
                detail=messages.ERROR_TOKEN,
            )
        if credentials.scheme.lower() != 'bearer':
            raise HTTPException(
                status_code=http.HTTPStatus.UNAUTHORIZED,
                detail=messages.ERROR_TOKEN_TYPE,
            )

        token = credentials.credentials
        decoded_token = self.parse_token(token)
        if not decoded_token:
            raise HTTPException(
                status_code=http.HTTPStatus.FORBIDDEN,
                detail=messages.ERROR_TOKEN,
            )

        # Проверка черного списка
        redis = await request.state.dishka_container.get(Redis)
        jti = decoded_token.get('jti')
        if jti and await redis.get(f'invalid_token:{jti}'):
            raise HTTPException(
                status_code=http.HTTPStatus.UNAUTHORIZED,
                detail=messages.TOKEN_IS_BLACKLISTED,
            )

        token_in_redis: bool = bool(
            await redis.get(f'access_token:{jti}') or await redis.get(f'refresh_token:{jti}'),
        )
        if jti and not token_in_redis:
            raise HTTPException(
                status_code=http.HTTPStatus.FORBIDDEN,
                detail=messages.ERROR_TOKEN,
            )

        return decoded_token

    @staticmethod
    def parse_token(jwt_token: str) -> dict[str, Any] | None:  # noqa: WPS602
        """*Decodes the given JWT token.*

        Returns:
            dict[str, Any] | None: decoded payload, or None if the token is invalid.
        """
        return decode_token(jwt_token)


security_jwt = JWTBearer()
