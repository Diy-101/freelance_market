from dataclasses import fields, is_dataclass
from enum import Enum
from typing import Any, Generic

from src.domain.types import EntityT, ModelT


class BaseMapper(Generic[EntityT, ModelT]):
    entity_class: type[EntityT]
    model_class: type[ModelT]

    def __init__(self, entity_class: type[EntityT], model_class: type):
        self.entity_class = entity_class
        self.model_class = model_class

    def entity_to_model(self, entity: EntityT):
        entity_dict = entity.to_dict()  # type: ignore

        model_fields = {c.name for c in self.model_class.__table__.columns}  # type: ignore
        filtered_data = {k: v for k, v in entity_dict.items() if k in model_fields}

        return self.model_class(**filtered_data)

    def dict_to_model(self, data: dict[str, Any]):
        model_columns = {c.name for c in self.model_class.__table__.columns}  # type: ignore
        filtered_data = {k: v for k, v in data.items() if k in model_columns}
        return self.model_class(**filtered_data)

    def dict_to_entity(self, data: dict[str, Any]):
        entity_fields = {f.name for f in fields(self.entity_class)}  # type: ignore
        filtered_data = {k: v for k, v in data.items() if k in entity_fields}
        return self.entity_class(**filtered_data)

    def model_to_dict(self, model: ModelT) -> dict[str, Any]:
        model_dict = {k: v for k, v in vars(model).items() if not k.startswith("_")}

        result = {}
        for key, value in model_dict.items():
            if isinstance(value, Enum):
                result[key] = value.value
            else:
                result[key] = value

        entity_fields = {f.name for f in fields(self.entity_class)}  # type: ignore
        filtered_data = {k: v for k, v in result.items() if k in entity_fields}
        return filtered_data

    def model_to_entity(self, model: ModelT) -> EntityT:
        filtered_data = self.model_to_dict(model)
        return self.dict_to_entity(filtered_data)


class MapperFactory:
    """Фабрика для создания мепперов для dataclasses"""

    _cache = {}

    @classmethod
    def get_mapper(
        cls, entity_class: type[EntityT], model_class: type[ModelT]
    ) -> BaseMapper[EntityT, ModelT]:
        if not is_dataclass(entity_class):
            raise TypeError(f"{entity_class} is not a dataclass")

        key = (entity_class, model_class)
        if key in cls._cache:  # type: ignore
            return cls._cache[key]  # type: ignore

        mapper = BaseMapper(entity_class, model_class)
        cls._cache[key] = mapper  # type: ignore
        return mapper
