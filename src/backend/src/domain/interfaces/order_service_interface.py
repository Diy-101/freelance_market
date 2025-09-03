from abc import ABC, abstractmethod

from src.domain.entities import Order


class OrderServiceInterface(ABC):
    """Interface for managing orders"""

    # ========== CRUD ===========
    @abstractmethod
    async def create_order(self, order: Order) -> Order:
        raise NotImplementedError

    @abstractmethod
    async def get_order_by_uuid(self, order_uuid: str) -> Order | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all_orders(self) -> list[Order]:
        raise NotImplementedError

    @abstractmethod
    async def update_order_by_uuid(self, order_uuid: str, new_data: Order) -> Order:
        raise NotImplementedError

    @abstractmethod
    async def delete_order_by_uuid(self, order_uuid: str) -> Order:
        raise NotImplementedError
