from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    tg_id: int
    first_name: str
    last_name: Optional[str] = None
    username: Optional[str] = None
    language_code: Optional[str] = None
    is_premium: Optional[bool] = None
    allows_write_to_pm: Optional[bool] = None
    photo_url: Optional[str] = None


class LoginResponse(BaseModel):
    user: User
    access_token: str
