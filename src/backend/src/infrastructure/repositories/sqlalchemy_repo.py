from typing import Any, get_type_hints

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.interfaces import AbstractRepository
from src.domain.types import EntityT, ModelT


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
    ):
        self._model = model
        self._entity = entity
        self._key_field = key_field
        self._factory_session = factory_session

    async def create(self, entity: dict[str, Any]) -> dict[str, Any]:
        async with self._factory_session() as session:
            model = self._model(**entity)  # type: ignore
            session.add(model)
            await session.commit()
            await session.refresh(model)

            entity_attrs = get_type_hints(self._entity)
            return {
                c.name: getattr(model, c.name)
                for c in self._model.__table__.columns  # type: ignore
                if c.name in entity_attrs
            }

    async def get_by_id(self, data_id: int | str) -> dict[str, Any] | None:
        async with self._factory_session() as session:
            stmt = select(self._model).where(
                getattr(self._model, self._key_field) == data_id
            )
            result = await session.execute(stmt)
            model = result.scalars().first()
            if model is None:
                return None

            entity_attrs = get_type_hints(self._entity)
            return {
                c.name: getattr(model, c.name)
                for c in self._model.__table__.columns  # type: ignore
                if c.name in entity_attrs
            }

    async def get_all(self) -> list[dict[str, Any]]:
        async with self._factory_session() as session:
            stmt = select(self._model)
            result = await session.execute(stmt)
            models = result.scalars().all()

            result = []
            entity_attrs = get_type_hints(self._entity)
            for model in models:
                model_dict = {
                    c.name: getattr(model, c.name)
                    for c in self._model.__table__.columns  # type: ignore
                    if c.name in entity_attrs
                }
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

            entity_attrs = get_type_hints(self._entity)
            return {
                c.name: getattr(model, c.name)
                for c in self._model.__table__.columns  # type: ignore
                if c.name in entity_attrs
            }

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

            entity_attrs = get_type_hints(self._entity)
            return {
                c.name: getattr(model, c.name)
                for c in self._model.__table__.columns  # type: ignore
                if c.name in entity_attrs
            }
