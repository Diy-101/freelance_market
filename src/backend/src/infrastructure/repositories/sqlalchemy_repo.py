from typing import Any

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.interfaces import AbstractRepository
from src.domain.types import EntityT, ModelT
from src.infrastructure.mapper import BaseMapper


class SQLAlchemyRepository(AbstractRepository[ModelT, EntityT]):
    """
    Универсальный репозиторий предоставляющий интерфейс SQLAlchemy для наследников
    """

    def __init__(
        self,
        model: type[ModelT],
        entity: type[EntityT],
        key_field: str,
        factory_session: async_sessionmaker[AsyncSession],
        mapper: BaseMapper,
    ):
        self._model = model
        self._entity = entity
        self._key_field = key_field
        self._factory_session = factory_session
        self._mapper = mapper

    async def create(self, entity: EntityT) -> dict[str, Any]:
        async with self._factory_session() as session:
            model = self._mapper.entity_to_model(entity)
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return self._mapper.model_to_dict(model)

    async def get_by_id(self, data_id: int | str) -> dict[str, Any] | None:
        async with self._factory_session() as session:
            stmt = select(self._model).where(
                getattr(self._model, self._key_field) == data_id
            )
            result = await session.execute(stmt)
            model = result.scalars().first()
            if model is None:
                return None
            return self._mapper.model_to_dict(model)

    async def get_all(self) -> list[dict[str, Any]]:
        async with self._factory_session() as session:
            stmt = select(self._model)
            result = await session.execute(stmt)
            models = result.scalars().all()

            result = []
            for model in models:
                model_dict = self._mapper.model_to_dict(model)
                result.append(model_dict)

            return result

    async def update(
        self, data_id: int | str, values: dict[str, Any]
    ) -> dict[str, Any]:
        async with self._factory_session() as session:
            stmt = (
                update(self._model)
                .where(getattr(self._model, self._key_field) == data_id)
                .values(**values)
                .returning(self._model)
            )
            result = await session.execute(stmt)
            model = result.scalars().first()

            if model is None:
                raise ValueError(
                    f"Can't be updated because entity with {data_id} id doesn't exist"
                )

            await session.commit()
            await session.refresh(model)

            return self._mapper.model_to_dict(model)

    async def delete(self, data_id: int | str) -> dict[str, Any]:
        async with self._factory_session() as session:
            stmt = select(self._model).where(
                getattr(self._model, self._key_field) == data_id
            )
            result = await session.execute(stmt)
            model = result.scalars().first()

            if model is None:
                raise ValueError(
                    f"Can't be deleted because entity with {data_id} id doesn't exist"
                )

            await session.delete(model)
            await session.refresh(model)

            return self._mapper.model_to_dict(model)
