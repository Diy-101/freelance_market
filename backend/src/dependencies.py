from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import create_session
from src.repository import SQLAlchemyRepository
from src.types import ModelT, SchemasT


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Создание сессии"""
    async with create_session() as session:
        yield session


def get_repository(model: type[ModelT], schema: type[SchemasT], key_field: str):
    return SQLAlchemyRepository(
        model, schema, key_field=key_field, factory_session=create_session
    )
