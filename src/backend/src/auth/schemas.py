from pydantic import BaseModel, Field

class InitDataSchema(BaseModel):
    init_data: str


class UserSchema(BaseModel):
    id: int = Field(alias="tg_id")
    is_bot: bool | None = None
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
    is_premium: bool | None = None
    added_to_attachment_menu: bool | None = None
    allows_write_to_pm: bool | None = None
    photo_url: str | None = None


class LoginSchema(BaseModel):
    user: UserSchema
    access_token: str