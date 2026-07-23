import logging
from typing import Any, cast

from jose import jwt

from app.common.messages import JWT_KEY_NOT_SET, SOME_JWT_ERROR
from app.core.config import settings


logger = logging.Logger(__name__)

def decode_token(token) -> dict | None:
    algorithm: str | None = settings.jwt.ALGORITHM.upper()
    key: str | None = settings.jwt.SECRET_KEY

    if not key:
        logger.error(JWT_KEY_NOT_SET)
        return None

    data = {
        'algorithms': algorithm,
        'audience': settings.jwt.JWT_AUTHJWT_DECODE_AUDIENCE
    }

    try:
        payload =jwt.decode(token, key, **data)
    except (jwt.ExpiredSignatureError, jwt.JWTError) as e:
        logger.error(SOME_JWT_ERROR.format(str(e)))
        return None

    return payload