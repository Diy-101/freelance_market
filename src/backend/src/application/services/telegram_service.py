import hashlib
import hmac
import json
from datetime import datetime, timezone
from typing import Dict
from urllib.parse import parse_qsl, unquote

from src.domain.entities import InitData, User
from src.domain.interfaces import TelegramServiceInterface
from src.domain.models import UserModel
from src.infrastructure.mapper import MapperFactory


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
        self._secret_key = self._generate_secret_key()
        self._mapper_factory = MapperFactory

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

    def _parse_user_data(self, user_json: str) -> dict[str, str]:
        """
        Парсит JSON данные пользователя
        """
        try:
            user_dict = json.loads(unquote(user_json, encoding="utf-8"))
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Failed to parse user data: {e}")
        return user_dict

    def _parse_init_data(self, init_data: str) -> dict[str, str]:
        """
        Парсит и валидирует initData от Telegram WebApp
        """
        try:
            # Парсим query string в raw данные
            raw_data = dict(parse_qsl(init_data, keep_blank_values=True))

            if not raw_data:
                raise ValueError("Empty init data")

            # Проверяем наличие hash
            if "hash" not in raw_data:
                raise ValueError("Missing hash field")

        except Exception as e:
            raise ValueError(f"Init data can't be parsed: {e}")
        return raw_data

    def validate_init_data(
        self, init_data: str, max_age_seconds: int = 86400
    ) -> InitData:
        """
        Валидирует initData с указанным максимальным возрастом
        """
        try:
            init_data_parsed = self._parse_init_data(init_data)

            data_check_string = self._create_data_check_string(init_data_parsed)
            calculated_hash = self._calculate_hash(data_check_string)
            received_hash = init_data_parsed["hash"]

            if not hmac.compare_digest(calculated_hash, received_hash):
                raise ValueError("Received hash is not valid")

            # Проверяем время (auth_date) с кастомным max_age
            if "auth_date" in init_data_parsed:
                try:
                    auth_date = int(init_data_parsed["auth_date"])
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

            user_dict = self._parse_user_data(init_data_parsed["user"])
            user = MapperFactory.get_mapper(User, UserModel).dict_to_entity(user_dict)

            return InitData(
                auth_date=int(init_data_parsed["auth_date"]),
                hash=init_data_parsed["hash"],
                user=user,
                query_id=init_data_parsed.get("hash"),
            )
        except Exception as e:
            raise ValueError(f"Can't validate initdata: {e}")
