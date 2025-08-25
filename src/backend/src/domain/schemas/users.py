from pydantic import BaseModel


class TelegramUser(BaseModel):
    tg_id: int
    is_bot: bool | None = None
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
    is_premium: bool | None = None
    added_to_attachment_menu: bool | None = None
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
    user: TelegramUser | None = None
    receiver: TelegramUser | None = None
    chat: TelegramChat | None = None
    chat_type: str | None = None
    chat_instance: str | None = None
    start_param: str | None = None
    can_send_after: int | None = None
    auth_date: int
    hash: str
    signature: str
