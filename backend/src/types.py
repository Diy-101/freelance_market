from typing import TypeVar

from pydantic import BaseModel

# Универсальный тип для работы с Sqlalchemy моделями
ModelT = TypeVar("ModelT")

# Универсальный тип для работы с Pydantic моделями
SchemasT = TypeVar("SchemasT", bound=BaseModel)
