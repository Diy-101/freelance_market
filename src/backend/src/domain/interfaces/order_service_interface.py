from abc import ABC, abstractmethod

class OrderInterface(ABC):
    """
    TODO: realize a order interface
    """
    @abstractmethod
    def __init__(self, repository):
        raise NotImplementedError

    # ========== CRUD ==========
    @abstractmethod
    async def get_order(self, order_id: int):
        raise NotImplementedError

