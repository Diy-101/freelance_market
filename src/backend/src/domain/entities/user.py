from dataclasses import dataclass

from dataclasses_json import dataclass_json

from src.domain.entities import BaseEntity


@dataclass_json
@dataclass
class User(BaseEntity):
    uuid: str
    tg_id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
    is_premium: bool = False
    allows_write_to_pm: bool | None = None
    photo_url: str | None = None
