import hashlib
import hmac
import json
from datetime import datetime, timezone
from typing import Any
from urllib.parse import parse_qsl, unquote

from src.domain.interfaces import TelegramServiceInterface
from src.settings import get_settings
from src.utils import logger

cfg = get_settings()


class TelegramService(TelegramServiceInterface):
    """
    Сервис для работы с Telegram WebApp API
    Инкапсулирует логику парсинга и валидации initData
    """

    def __init__(self, bot_token: str):
        """
        Инициализация сервиса с токеном бота
        """
        self.bot_token = bot_token

    def validate_init_data(
        self, init_data: str, max_age_seconds: int = 86400
    ) -> dict[str, Any]:
        """
        Валидирует initData с указанным максимальным возрастом
        """
        try:
            # Check hash
            vals = {k: v for k, v in parse_qsl(init_data)}

            received_hash = vals["hash"]
            data_check_string = "\n".join(
                f"{k}={v}" for k, v in sorted(vals.items()) if k != "hash"
            )

            secret_key = hmac.new(
                "WebAppData".encode(), cfg.bot_token.encode(), hashlib.sha256
            ).digest()
            calculated_hash = hmac.new(
                secret_key, data_check_string.encode(), hashlib.sha256
            ).hexdigest()

            if cfg.debug:
                logger.debug(f"data_check_string: {data_check_string}")
                logger.debug(f"calculated_hash: {calculated_hash}")
                logger.debug(f"received_hash: {received_hash}")

            if not hmac.compare_digest(calculated_hash, received_hash):
                raise ValueError("Received hash is not valid")

            # Parse init_data
            user_dict = json.loads(unquote(vals["user"]))
            user_dict["tg_id"] = user_dict["id"]
            user_dict["is_premium"] = False
            del user_dict["id"]

            if cfg.debug:
                logger.debug(f"user_dict: {user_dict}")

            # Проверяем время (auth_date) с кастомным max_age
            if "auth_date" in vals:
                try:
                    auth_date = int(vals["auth_date"])
                    current_timestamp = int(datetime.now(timezone.utc).timestamp())

                    if current_timestamp - auth_date > max_age_seconds:
                        raise ValueError(
                            f"Data is too old. Auth date: {auth_date}, "
                            f"Current: {current_timestamp}, "
                            f"Difference: {current_timestamp - auth_date} "
                            f"Max age: {max_age_seconds}s"
                        )
                except ValueError as e:
                    raise ValueError(f"Invalid auth_date: {e}")

            return {
                "auth_date": int(vals["auth_date"]),
                "hash": vals["hash"],
                "user": user_dict,
                "query_id": vals.get("query_id"),
            }
        except Exception as e:
            if cfg.debug:
                logger.error(f"Error: {e}")
            raise ValueError(f"Can't validate initdata: {e}")
