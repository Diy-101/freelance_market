from dataclasses import dataclass
from typing import Any

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class BaseEntity:
    def to_dict(self, exclude: list[str] | None = None) -> dict[str, Any]:
        """Custom method to serialize the entity to dict, excluding optional fields if specified."""
        data = self.to_dict()
        if exclude:
            for key in exclude:
                data.pop(key, None)
        return data
