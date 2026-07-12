from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.database import DatabaseSettings
from app.core.env import ENV_FILE_PATH


class Settings(BaseSettings):
    project_name: str

    db: DatabaseSettings = DatabaseSettings()  # type: ignore

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding='utf-8',
        env_prefix='MONO_',
        extra='ignore',
    )


settings = Settings()
