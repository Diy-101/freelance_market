from pydantic import BaseModel
from aiogram.utils.web_app import WebAppUser

class SignIn(BaseModel):
    access_token: str
    refresh_token: str
    user: WebAppUser

class InitData(BaseModel):
    init_data: str