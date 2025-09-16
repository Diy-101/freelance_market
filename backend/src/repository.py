from typing import Any, Generic

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.types import ModelT, SchemasT


class SQLAlchemyRepository(Generic[ModelT, SchemasT]):
    """
    Универсальный репозиторий предоставляющий интерфейс SQLAlchemy
    """

    def __init__(
        self,
        model: type[ModelT],
        schema: type[SchemasT],
        key_field: str,
        factory_session: async_sessionmaker[AsyncSession],
    ):
        self._model = model
        self._schema = schema
        self._key_field = key_field
        self._factory_session = factory_session

    async def create(self, schema: SchemasT) -> str:  # Return ID written to the DB
        async with self._factory_session() as session:
            model = self._model(**schema.model_dump())
            session.add(model)
            await session.commit()
            await session.refresh(model)
            return model.id  # type: ignore

    async def get_by_id(self, data_id: int | str) -> SchemasT | None:
        async with self._factory_session() as session:
            stmt = select(self._model).where(
                getattr(self._model, self._key_field) == data_id
            )
            result = await session.execute(stmt)
            model = result.scalars().first()
            if model is None:
                return None

            return self._schema.model_validate(model)

    async def get_all(self) -> list[SchemasT]:
        async with self._factory_session() as session:
            stmt = select(self._model)
            result = await session.execute(stmt)
            models = result.scalars().all()

            result = []
            for model in models:
                schema = self._schema.model_validate(model)
                result.append(schema)

            return result

    async def update(self, data_id: int | str, values: dict[str, Any]) -> SchemasT:
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
                    f"Can't be updated because schema with {data_id} id doesn't exist"
                )

            await session.commit()
            await session.refresh(model)
            return self._schema.model_validate(model)

    async def delete(self, data_id: int | str) -> SchemasT:
        async with self._factory_session() as session:
            stmt = select(self._model).where(
                getattr(self._model, self._key_field) == data_id
            )
            result = await session.execute(stmt)
            model = result.scalars().first()

            if model is None:
                raise ValueError(
                    f"Can't be deleted because schema with {data_id} id doesn't exist"
                )

            await session.delete(model)
            await session.refresh(model)
            return self._schema.model_validate(model)
