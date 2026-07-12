from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.env import ENV_FILE_PATH


class DatabaseSettings(BaseSettings):
    USER: str
    PASSWORD: str
    HOST: str
    DB: str
    PORT: int

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding='utf-8',
        env_prefix='POSTGRES_',
        extra='ignore'
    )

    @property
    def database_url(self) -> str:
        return (
            f'postgresql+asyncpg://{self.USER}:{self.PASSWORD}'
            f'@{self.HOST}:{self.PORT}/{self.DB}'
        )
