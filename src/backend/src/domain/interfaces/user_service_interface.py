from abc import ABC, abstractmethod
from typing import Callable

from src.domain.entities import User


class UserServiceInterface(ABC):
    """Интерфейс для управдения пользователями и аутентификацией"""

    # ============ CRUD ============
    @abstractmethod
    async def create_user(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_tg_id(self, user_id: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_users(self) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    async def update_user_by_tg_id(self, user_id: int, new_data: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def delete_user_by_tg_id(self, user_id: int) -> User:
        raise NotImplementedError

    # ============= Аутентификация и авторизация =============
    @abstractmethod
    def create_token(self, user_id: int) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_token_dependency(self) -> Callable:
        raise NotImplementedError
