from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters import PyJWTAdapter
from src.database import create_session
from src.domain.interfaces.jwt_interface import JWTInterface
from src.repositories.abstract import AbstractRepository
from src.repositories.user_repo import UserRepository
from src.services import UserService
from src.settings import get_settings
from src.utils.telegram_validator import TelegramValidator


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
        def create_orders_repo():
            pass

    return RepositoryFactory()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Создание сессии"""
    async with create_session() as session:
        yield session


def get_telegram_validator() -> TelegramValidator:
    return TelegramValidator(get_settings().bot_token, max_age_seconds=1000000)


def get_user_service() -> UserService:
    """Получение UserService"""
    repo = get_repository_factory().create_user_repo()
    adapter = get_jwt_adapter()
    validator = get_telegram_validator()
    return UserService(repo, adapter, validator)
