from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.entities import Order
from src.domain.models import OrderModel

from .sqlalchemy_repo import SQLAlchemyRepository


class OrderRepository(SQLAlchemyRepository[OrderModel, Order]):
    """
    Репозиторий для работы с таблицей orders
    """

    def __init__(self, factory_session: async_sessionmaker[AsyncSession]):
        super().__init__(
            model=OrderModel,
            entity=Order,
            factory_session=factory_session,
            key_field="uuid",
        )
