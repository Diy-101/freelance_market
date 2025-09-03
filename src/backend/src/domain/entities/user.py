from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class User:
    tg_id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
    allows_write_to_pm: bool | None = None
    photo_url: str | None = None
    uuid: str = field(default_factory=lambda: str(uuid4()), init=False)
