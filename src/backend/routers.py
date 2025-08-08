from fastapi import Header, APIRouter
from bot import dp, bot
import logging
from typing import Annotated
from aiogram import types

from settings import get_settings

cfg = get_settings()


telegram_router = APIRouter(
    prefix="",
    tags=["root"],
    responses={404: {"description": "Not found!"}}
)

@telegram_router.get("/")
async def root() -> dict:
    return {"ok": True}

@telegram_router.post(cfg.webhook_path)
async def bot_webhook(
    update: dict,
    x_telegram_bot_api_secret_token: Annotated[str, Header()]):
    if x_telegram_bot_api_secret_token != cfg.my_telegram_token:
        logging.error("Wrong secret token !")
        return {"error": "you don't have access"}
    telegram_update = types.Update(**update)
    if cfg.debug:
        logging.info(f"Telegram update: {telegram_update}")
    await dp.feed_webhook_update(bot=bot, update=telegram_update)