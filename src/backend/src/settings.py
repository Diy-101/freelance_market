from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    bot_token: str
    webhook_path: str
    webhook_url: str
    debug: bool
    my_telegram_token: str
    database_url: str
    secret_key_jwt: str
    algorithm_jwt: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()
