import hashlib
import hmac
import json
from datetime import datetime, timezone
from typing import Dict
from urllib.parse import parse_qsl, unquote

from src.domain.schemas.users import TelegramInitData


class TelegramValidator:
    """
    Валидатор для Telegram WebApp initData
    Обрабатывает URL-encoded JSON поля и валидирует подпись
    """

    def __init__(self, bot_token: str, max_age_seconds: int = 86400):
        self.bot_token = bot_token
        self._secret_key = self._generate_secret_key()

    def _generate_secret_key(self) -> bytes:
        """
        Генерирует секретный ключ: HMAC_SHA256(<bot_token>, "WebAppData")
        """
        return hmac.new(
            key="WebAppData".encode("utf-8"),
            msg=self.bot_token.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).digest()

    def _create_data_check_string(self, data: Dict[str, str]) -> str:
        """
        Создает data-check-string из параметров (исключая hash)
        Сортирует по алфавиту и объединяет через \n
        """
        # Исключаем hash из проверки
        filtered_data = {k: v for k, v in data.items() if k != "hash"}

        # Сортируем по ключам и создаем строку key=value
        sorted_pairs = sorted(filtered_data.items())
        data_check_string = "\n".join([f"{key}={value}" for key, value in sorted_pairs])

        return data_check_string

    def _calculate_hash(self, data_check_string: str) -> str:
        """
        Вычисляет HMAC-SHA256 хеш для data-check-string
        """
        return hmac.new(
            key=self._secret_key,
            msg=data_check_string.encode("utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()

    def parse_init_data(self, init_data: str) -> TelegramInitData:
        """
        Парсит и декодирует initData query string
        """
        # Парсим query string
        raw_data = dict(parse_qsl(init_data, keep_blank_values=True))

        result = {}

        for key, value in raw_data.items():
            if key in ["user", "receiver", "chat"]:
                try:
                    # URL-decode и парсим JSON
                    decoded_json = unquote(value)
                    result[key] = json.loads(decoded_json)
                    result[key]["tg_id"] = result[key]["id"]
                    del result[key]["id"]
                except (json.JSONDecodeError, ValueError) as e:
                    print(f"Failed to parse JSON for key '{key}': {e}")
                    result[key] = (
                        value  # Оставляем как строку если не удалось распарсить
                    )
            else:
                # Обычные поля (auth_date, query_id, hash, etc.)
                result[key] = value



        return TelegramInitData(**result)

    def validate_init_data(
        self, init_data: str, max_age_seconds: int = 86400
    ) -> TelegramInitData:
        """
        Полная валидация initData от Telegram WebApp
        """
        try:
            # Парсим query string в raw данные (без декодирования JSON)
            raw_data = dict(parse_qsl(init_data, keep_blank_values=True))

            if not raw_data:
                raise ValueError("Empty init data")

            # Проверяем наличие hash
            if "hash" not in raw_data:
                raise ValueError("Missing hash field")

            received_hash = raw_data["hash"]

            # Создаем data-check-string из RAW данных (до декодирования JSON!)
            data_check_string = self._create_data_check_string(raw_data)

            # Вычисляем ожидаемый hash
            expected_hash = self._calculate_hash(data_check_string)

            # Сравниваем хеши
            if not hmac.compare_digest(received_hash, expected_hash):
                raise ValueError(
                    f"Hash validation failed. Expected: {expected_hash}, "
                    f"Received: {received_hash}"
                )

            # Проверяем время (auth_date)
            if "auth_date" in raw_data:
                try:
                    auth_date = int(raw_data["auth_date"])
                    current_timestamp = int(datetime.now(timezone.utc).timestamp())

                    if current_timestamp - auth_date > max_age_seconds:
                        raise ValueError(
                            f"Data is too old. Auth date: {auth_date}, "
                            f"Current: {current_timestamp}, "
                            f"Max age: {max_age_seconds}s"
                        )
                except ValueError as e:
                    raise ValueError(f"Invalid auth_date: {e}")

            # Теперь декодируем JSON поля для удобства использования
            parsed_data = self.parse_init_data(init_data)

            return parsed_data

        except Exception as e:
            raise ValueError(f"Init data validation failed: {str(e)}")
