from fastapi import Header, APIRouter
from src.bot import dp, bot
from src.utils.logger import logger
from typing import Annotated
from aiogram import types

from src.settings import get_settings

cfg = get_settings()


webhook = APIRouter(
    prefix="/api",
    tags=["root"],
    responses={404: {"description": "Not found!"}}
)

@webhook.post(cfg.webhook_path)
async def bot_webhook(
    update: dict,
    x_telegram_bot_api_secret_token: Annotated[str, Header()]
):
    if x_telegram_bot_api_secret_token != cfg.my_telegram_token:
        logger.error("Wrong secret token !")
        return {"error": "you don't have access"}
    telegram_update = types.Update(**update)
    if cfg.debug:
        logger.info(f"Type: {type(update), update}")
        logger.info(f"Telegram update: {telegram_update}")
    await dp.feed_webhook_update(bot=bot, update=telegram_update)