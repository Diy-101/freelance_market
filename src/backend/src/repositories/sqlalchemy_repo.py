from typing import Any

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.domain.types import ModelT, SchemaT

from .abstract import AbstractRepository


class SQLAlchemyRepository(AbstractRepository[ModelT, SchemaT]):
    """
    Универсальный репозиторий предоставляющий интерфейс SQLAlchemy для наследников
    """

    def __init__(
        self,
        model: type[ModelT],
        schema: type[SchemaT],
        factory_session: async_sessionmaker[AsyncSession],
        key_field: str,
    ):
        self._factory_session = factory_session
        self._model = model
        self._schema = schema
        self._key_field = key_field

    async def create(self, data: SchemaT) -> SchemaT:
        async with self._factory_session() as session:
            new_user = self._model(**data.model_dump())
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return self._schema.model_validate(new_user, from_attributes=True)

    async def get(self, data_id: int) -> SchemaT | None:
        async with self._factory_session() as session:
            stmt = select(self._model).where(getattr(self._model, self._key_field) == data_id)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            if user is None:
                return None
            return self._schema.model_validate(user, from_attributes=True)

    async def update(self, data_id: int, values: dict[str, Any]) -> SchemaT | None:
        async with self._factory_session() as session:
            stmt = (
                update(self._model)
                .where(getattr(self._model, self._key_field) == data_id)
                .values(**values)
                .returning(self._model)
            )
            updated_user = await session.execute(stmt)
            updated_user = updated_user.scalar_one_or_none()
            if updated_user is None:
                return None
            await session.commit()
            await session.refresh(updated_user)
            return self._schema.model_validate(updated_user, from_attributes=True)

    async def delete(self, data_id: int) -> int | None:
        async with self._factory_session() as session:
            stmt = select(self._model).where(getattr(self._model, self._key_field) == data_id)
            result = await session.execute(stmt)
            result = result.scalars().first()

            if result is None:
                return None

            await session.delete(result)
            await session.commit()
            return self._schema.model_validate(result, from_attributes=True)