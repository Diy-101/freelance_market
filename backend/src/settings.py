from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str
    webhook_path: str
    webhook_url: str
    debug: bool
    my_telegram_token: str
    database_url: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_adapter: str
    mock_user: str
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    """
    Получение настроек приложения
    """
    return Settings()  # type: ignore
