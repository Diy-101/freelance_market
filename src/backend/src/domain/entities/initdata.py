from dataclasses import dataclass

from dataclasses_json import dataclass_json

from .user import User


@dataclass_json
@dataclass
class InitData:
    auth_date: int  # Unix time
    hash: str
    user: User
    query_id: str | None = None
