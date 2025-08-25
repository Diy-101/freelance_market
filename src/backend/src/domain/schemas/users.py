from pydantic import BaseModel


class User(BaseModel):
    tg_id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
    allows_write_to_pm: bool | None = None
    photo_url: str | None = None


class TelegramChat(BaseModel):
    id: int
    tg_id: int
    type: str
    title: str
    username: str | None = None
    photo_url: str | None = None


class TelegramInitData(BaseModel):
    query_id: str | None = None
    user: User | None = None
    receiver: User | None = None
    chat: TelegramChat | None = None
    chat_type: str | None = None
    chat_instance: str | None = None
    start_param: str | None = None
    can_send_after: int | None = None
    auth_date: int
    hash: str
    signature: str
