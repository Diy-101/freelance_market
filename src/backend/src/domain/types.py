from typing import TypeVar

# Универсальный тип для работы с моделями ?(Sqlalchemy)
ModelT = TypeVar("ModelT")

# Универсальный тип для работы с domain entities
EntityT = TypeVar("EntityT")

# Универсальный тип для работы со схемами (Pydantic BaseModel)
SchemaT = TypeVar("SchemaT")
