import http
from typing import Any

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

from app.common import messages
from app.utils.security import decode_token


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict[str, Any]:
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
    def parse_token(jwt_token: str) -> Dict[str, Any] | None:  # noqa: WPS602
        """
        Функция декодирования JWT-токена.

        Args:
            jwt_token: Токен.

        Returns:
            dict: словарь с расшифрованными данными.
        """
        return decode_token(jwt_token)

security_jwt = JWTBearer()
