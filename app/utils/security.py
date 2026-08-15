import logging

from jose import jwt

from app.common.messages import JWT_KEY_NOT_SET, SOME_JWT_ERROR
from app.core.config import settings

logger = logging.Logger(__name__)


def decode_token(token) -> dict | None:
    """*Decodes and validates a JWT token with the configured secret key and algorithm.*

    Returns:
        dict | None: token payload, or None if the key is not set or the token is
            expired/invalid.
    """
    algorithm: str | None = settings.jwt.ALGORITHM.upper()
    key: str | None = settings.jwt.SECRET_KEY

    if not key:
        logger.error(JWT_KEY_NOT_SET)
        return None

    data = {'algorithms': algorithm, 'audience': settings.jwt.JWT_AUTHJWT_DECODE_AUDIENCE}

    try:
        payload = jwt.decode(token, key, **data)
    except (jwt.ExpiredSignatureError, jwt.JWTError) as e:
        logger.error(SOME_JWT_ERROR.format(str(e)))
        return None

    return payload
