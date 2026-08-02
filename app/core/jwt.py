from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.env import ENV_FILE_PATH


class JWTSettings(BaseSettings):
    """*JWT settings loaded from the environment with the `JWT_` prefix.*"""

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRES: int
    REFRESH_TOKEN_EXPIRES: int
    ALGORITHM: str = 'HS256'
    JWT_AUTHJWT_DECODE_AUDIENCE: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_prefix='JWT_',
        extra='ignore',
        env_file_encoding='utf-8',
    )
