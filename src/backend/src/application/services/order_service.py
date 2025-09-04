from src.domain.entities import Order
from src.domain.interfaces import AbstractRepository, OrderServiceInterface
from src.domain.models import OrderModel


class OrderService(OrderServiceInterface):
    def __init__(self, order_repository: AbstractRepository[OrderModel, Order]):
        self._repository = order_repository
        self._order_model = OrderModel

    async def create_order(self, order: Order) -> Order:
        order_dict = await self._repository.create(order)  # TODO: change entity to dict
        return self._mapper.dict_to_entity(order_dict)

    async def get_order_by_uuid(self, order_uuid: str) -> Order | None:
        order_dict = await self._repository.get_by_id(order_uuid)

        if order_dict is not None:
            return self._mapper.dict_to_entity(order_dict)
        return None

    async def get_all_orders(self) -> list[Order]:
        orders_dict = await self._repository.get_all()

        orders = []
        for order_dict in orders_dict:
            order = self._mapper.dict_to_entity(order_dict)
            orders.append(order)

        return orders

    async def update_order_by_uuid(self, order_uuid: str, new_data: Order) -> Order:
        current_order_dict = await self._repository.get_by_id(order_uuid)
        if current_order_dict is None:
            raise ValueError(f"The order with {order_uuid} uuid doesn't exist")

        try:
            new_data_dict = new_data.to_dict()  # type: ignore
            fields_to_update = {
                f: new_val
                for f, curr_val in current_order_dict.items()
                for _, new_val in new_data_dict.items()
                if curr_val != new_val
            }
        except Exception as e:
            raise ValueError(f"Can't map the fields: {e}")

        if fields_to_update:
            updated_order_dict = await self._repository.update(
                order_uuid, fields_to_update
            )
            return self._mapper.dict_to_entity(updated_order_dict)
        return self._mapper.dict_to_entity(current_order_dict)

    async def delete_order_by_uuid(self, order_uuid: str) -> Order:
        try:
            deleted_order_dict = await self._repository.delete(order_uuid)
        except Exception as e:
            raise ValueError(
                f"Can't delete the order with the following {order_uuid} uuid: {e}"
            )
        return self._mapper.dict_to_entity(deleted_order_dict)
