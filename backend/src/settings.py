import sys
from functools import lru_cache
from os import getenv

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    bot_token: str = getenv("BOT_TOKEN")
    webhook_path: str = getenv("WEBHOOK_PATH")
    webhook_url: str = getenv("WEBHOOK_URL")
    my_telegram_token: str = getenv("MY_TELEGRAM_TOKEN")
    database_url: str = getenv("DATABASE_URL")
    jwt_secret_key: str = getenv("JWT_SECRET_KEY")
    jwt_algorithm: str = getenv("JWT_ALGORITHM")
    debug: bool = getenv("DEBUG")


@lru_cache
def get_settings() -> Settings:
    """
    Get app settings
    """
    try:
        settings = Settings()  # type: ignore
    except Exception as e:
        print(f"Environmental variables didn't set: {e}")
        sys.exit(1)
    return settings
