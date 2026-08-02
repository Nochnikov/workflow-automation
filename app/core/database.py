from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.env import ENV_FILE_PATH


class DatabaseSettings(BaseSettings):
    """*PostgreSQL connection settings loaded from the environment with the `POSTGRES_` prefix.*"""

    USER: str
    PASSWORD: str
    HOST: str
    DB: str
    PORT: int

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding='utf-8',
        env_prefix='POSTGRES_',
        extra='ignore',
    )

    @property
    def database_url(self) -> str:
        """*Builds the asyncpg SQLAlchemy DSN from the configured credentials.*

        Returns:
            str: database URL in the `postgresql+asyncpg://` format.
        """
        return f'postgresql+asyncpg://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DB}'
