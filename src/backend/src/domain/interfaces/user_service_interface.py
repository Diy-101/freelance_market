from abc import ABC, abstractmethod
from typing import Callable

from src.domain.schemas.users import TelegramInitData, User


class UserServiceInterface(ABC):
    """
    Интерфейс для управдения пользователями и аутентификацией
    """

    @abstractmethod
    def __init__(self, repository, jwt_adapter) -> None:
        """
        Инициализация сервиса с репозиторием и JWT адаптером
        """
        raise NotImplementedError

    # ============ CRUD ============
    @abstractmethod
    async def create_user(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_user(self, user_id: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def update_user(self, user_id: str, values: User) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_user(self, user_id: str) -> User | None:
        raise NotImplementedError

    # ============= Аутентификация и авторизация =============
    @abstractmethod
    def check_init_data(self, init_data: str) -> TelegramInitData:
        """
        Проверка Telegram initData
        """
        raise NotImplementedError

    @abstractmethod
    def authenticate_user_from_init_data(self, init_data: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def create_token(self, user_id) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_token_dependency(self) -> Callable:
        """
        Возвращает dependency для проверки JWT токена в FastAPI
        """
        raise NotImplementedError

    @abstractmethod
    async def get_current_user_from_token(self, token_data: dict) -> User:
        """
        Получение текущего пользователя из данных токена
        """
        raise NotImplementedError
