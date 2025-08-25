from abc import ABC, abstractmethod
from typing import Any, Callable


class JWTInterface(ABC):
    @abstractmethod
    def __init__(self):
        """
        Инициализирует адаптер для работы с JWT токенами
        """
        raise NotImplementedError

    @abstractmethod
    def create_access_token(self, uid: str) -> str:
        """
        Создает JWT токен доступа
        """
        raise NotImplementedError

    @abstractmethod
    def token_required(self) -> Callable[..., Any]:
        """
        Зависимость для проверки JWT токена.
        Возвращает callable, который FastAPI использует в Depends()
        """
        raise NotImplementedError
