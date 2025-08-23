from pydantic import BaseModel

from src.domain.schemas.users import TelegramUser


class LoginResponse(BaseModel):
    user: TelegramUser
    access_token: str
