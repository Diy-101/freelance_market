from typing import TypeVar

from pydantic import BaseModel

# Универсальный тип для работы с моделями ?(Sqlalchemy)
ModelT = TypeVar("ModelT")

# Универсальный тип для работы со схемами pydantic
SchemaT = TypeVar("SchemaT", bound=BaseModel)
