from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services import UserService
from src.application.services.order_service import OrderService
from src.application.services.telegram_service import TelegramService
from src.database import create_session
from src.domain.interfaces.jwt_interface import JWTInterface
from src.infrastructure.adapters.pyjwt_adapter import PyJWTAdapter
from src.domain.interfaces.repository_interface import AbstractRepository
from src.infrastructure.repositories.user_repo import UserRepository
from src.infrastructure.repositories.order_repo import OrderRepository
from src.settings import get_settings


def get_jwt_adapter() -> JWTInterface:
    """Получение адаптера для JWT токенов"""
    settings = get_settings()
    adapter_type = getattr(settings, "jwt_adapter", "pyjwt")

    match adapter_type:
        case "pyjwt":
            return PyJWTAdapter()
        case _:
            raise ValueError("Unknown adapter type")


def get_repository_factory():
    """Фабрика для создания репозиториев"""
    session_factory = create_session

    class RepositoryFactory:
        @staticmethod
        def create_user_repo() -> AbstractRepository:
            return UserRepository(session_factory)

        @staticmethod
        def create_orders_repo() -> AbstractRepository:
            return OrderRepository(session_factory)

    return RepositoryFactory()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Создание сессии"""
    async with create_session() as session:
        yield session


def get_telegram_service() -> TelegramService:
    """Получение TelegramService"""
    return TelegramService(get_settings().bot_token)


def get_user_service() -> UserService:
    """Получение UserService"""
    repo = get_repository_factory().create_user_repo()
    adapter = get_jwt_adapter()
    return UserService(repo, adapter)


def get_order_service() -> OrderService:
    """Получение OrderService"""
    repo = get_repository_factory().create_orders_repo()
    return OrderService(repo)
