from abc import ABC, abstractmethod
from typing import Any, Generic

from src.domain.types import EntityT, ModelT


class AbstractRepository(ABC, Generic[ModelT, EntityT]):
    @abstractmethod
    def __init__(self, model: type[ModelT], entity: type[EntityT]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def create(self, entity: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, data_id: str | int) -> dict[str, Any] | None:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    async def update(
        self, data_id: str | int, values: dict[str, Any]
    ) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, data_id: str | int) -> dict[str, Any]:
        raise NotImplementedError
