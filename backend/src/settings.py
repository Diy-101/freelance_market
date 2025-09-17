from functools import lru_cache
from os import getenv

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    bot_token = getenv("BOT_TOKEN")
    webhook_path = getenv("WEBHOOK_PATH")
    webhook_url = getenv("WEBHOOK_URL")
    my_telegram_token = getenv("MY_TELEGRAM_TOKEN")
    database_url = getenv("DATABASE_URL")
    jwt_secret_key = getenv("JWT_SECRET_KEY")
    jwt_algorithm = getenv("JWT_ALGORITHM")
    jwt_adapter = getenv("JWT_ADAPTER")
    debug = getenv("DEBUG")


@lru_cache
def get_settings() -> Settings:
    """
    Get app settings
    """
    return Settings()  # type: ignore
