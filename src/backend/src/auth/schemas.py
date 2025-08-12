from pydantic import BaseModel
from aiogram.utils.web_app import WebAppUser

class SignIn(BaseModel):
    user: WebAppUser
    access_token: str

class InitData(BaseModel):
    init_data: str