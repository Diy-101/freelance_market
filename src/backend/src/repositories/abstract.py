from abc import ABC, abstractmethod
from typing import Any, Generic

from src.domain.types import ModelT, SchemaT


class AbstractRepository(ABC, Generic[ModelT, SchemaT]):
    @abstractmethod
    def __init__(self, model: type[ModelT], schema: type[SchemaT]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def create(self, data: SchemaT) -> SchemaT:
        raise NotImplementedError

    @abstractmethod
    async def get(self, data_id: int) -> SchemaT | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, data_id: int, values: dict[str, Any]) -> SchemaT | None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, data_id: int) -> SchemaT | None:
        raise NotImplementedError
