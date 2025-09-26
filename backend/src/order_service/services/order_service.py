from typing import List, Optional

from src.order_service.models.orders import OrderModel
from src.order_service.schemas.orders import Order
from src.repository import get_repository


class OrderService:
    """Service for managing orders"""

    def __init__(self):
        self._repository = get_repository(OrderModel, Order, "uuid")

    async def create_order(self, order: Order) -> Order:
        """Create a new order"""
        order_id = await self._repository.create(order)
        return await self.get_order_by_uuid(order_id)

    async def get_order_by_uuid(self, order_id: str) -> Optional[Order]:
        """Get order by UUID"""
        return await self._repository.get_by_id(order_id)

    async def get_all_orders(self) -> List[Order]:
        """Get all orders"""
        return await self._repository.get_all()

    async def update_order_by_uuid(self, order_id: str, order: Order) -> Order:
        """Update order by UUID"""
        values = {
            k: v for k, v in order.model_dump().items() if v is not None and k != "uuid"
        }
        return await self._repository.update(order_id, values)

    async def delete_order_by_uuid(self, order_id: str) -> Order:
        """Delete order by UUID"""
        return await self._repository.delete(order_id)
