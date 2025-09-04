from abc import ABC, abstractmethod
from typing import Any


class TelegramServiceInterface(ABC):
    """
    Интерфейс для работы с Telegram WebApp API
    """

    @abstractmethod
    def __init__(self, bot_token: str) -> None:
        """
        Инициализация сервиса с токеном бота
        """
        raise NotImplementedError

    @abstractmethod
    def validate_init_data(
        self, init_data: str, max_age_seconds: int = 86400
    ) -> dict[str, Any]:
        """
        Валидирует initData с указанным максимальным возрастом
        """
        raise NotImplementedError
