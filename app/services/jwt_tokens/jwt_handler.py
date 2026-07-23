import datetime
import uuid

from async_fastapi_jwt_auth import AuthJWT

from app.core.config import settings
from app.services.jwt_tokens.base import JWTHandlerABC


class JWTHandler(JWTHandlerABC):

    def __init__(self, auth_jwt: AuthJWT):
        self._auth_jwt = auth_jwt

    async def create_access_token(self, user_id: int, claims: dict) -> tuple[str, str]:
        access_jti = str(uuid.uuid4())
        token = await self._auth_jwt.create_access_token(
            subject=str(user_id),
            user_claims={**claims, 'access_jit': access_jti},
            fresh=True,
            expires_time=datetime.timedelta(seconds=settings.jwt.ACCESS_TOKEN_EXPIRES),
        )
        return token, access_jti

    async def create_refresh_token(self, user_id: int, access_jti: str) -> tuple[str, str]:
        refresh_jti = str(uuid.uuid4())
        refresh_claims = {'access_jti': access_jti, 'jti': refresh_jti}

        if settings.jwt.JWT_AUTHJWT_DECODE_AUDIENCE:
            refresh_claims['aud'] = settings.jwt.JWT_AUTHJWT_DECODE_AUDIENCE


        token = await self._auth_jwt.create_refresh_token(
            subject=str(user_id),
            user_claims=refresh_claims,
            expires_time=datetime.timedelta(seconds=settings.jwt.REFRESH_TOKEN_EXPIRES),
        )
        return token, refresh_jti
