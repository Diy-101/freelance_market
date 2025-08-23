from typing import Annotated

from aiogram import types
from fastapi import APIRouter, Header

from src.bot import bot, dp
from src.settings import get_settings
from src.utils.logger import logger

cfg = get_settings()

webhook_router = APIRouter(
    prefix="", tags=["root"], responses={404: {"description": "Not found!"}}
)


@webhook_router.post(cfg.webhook_path)
async def bot_webhook(
    update: dict, x_telegram_bot_api_secret_token: Annotated[str, Header()]
):
    if x_telegram_bot_api_secret_token != cfg.my_telegram_token:
        logger.error("Wrong secret token!")
        return {"error": "you don't have access"}
    telegram_update = types.Update(**update)
    if cfg.debug:
        logger.info(f"Type: {type(update), update}")
        logger.info(f"Telegram update: {telegram_update}")
    await dp.feed_webhook_update(bot=bot, update=telegram_update)
