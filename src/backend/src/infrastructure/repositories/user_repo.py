from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.entities import User
from src.domain.models import UserModel

from .sqlalchemy_repo import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository[UserModel, User]):
    """
    Репозиторий для работы с таблицей users
    """

    def __init__(self, factory_session: async_sessionmaker[AsyncSession]):
        super().__init__(
            model=UserModel,
            entity=User,
            factory_session=factory_session,
            key_field="tg_id",
        )
