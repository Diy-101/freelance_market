from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.models.users import UserModel
from src.domain.schemas.users import TelegramUser
from .sqlalchemy_repo import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository[UserModel, TelegramUser]):
    """
    Репозиторий для работы с таблицей users
    """

    def __init__(self, factory_session: async_sessionmaker[AsyncSession]):
        super().__init__(model=UserModel, schema=TelegramUser, factory_session=factory_session)
