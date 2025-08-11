from aiogram import Dispatcher, Bot, Router
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, WebhookInfo
from aiogram.client.default import DefaultBotProperties

from src.utils.logger import logger
import os
from src.settings import get_settings, Settings

cfg: Settings = get_settings()

telegram_router = Router(name="telegram_router")
dp = Dispatcher()

dp.include_router(telegram_router)
bot = Bot(token=cfg.bot_token, default=DefaultBotProperties(
    parse_mode=ParseMode.HTML,
))

# Functions
async def check_webhook(my_bot: Bot) -> WebhookInfo | None:
    try:
        webhook_info = await my_bot.get_webhook_info()
        return webhook_info
    except Exception as e:
        logger.error(f"App can't get webhook_info\nError: {e}")

async def set_webhook(my_bot: Bot) -> None:
    current_webhook = await check_webhook(my_bot=my_bot)

    if cfg.debug:
        logger.debug(f"Current bot info: {current_webhook}")

    try:
        await my_bot.set_webhook(
            url=f"{cfg.webhook_url}{cfg.webhook_path}",
            secret_token=cfg.my_telegram_token,
            max_connections=40 if cfg.debug else 100,
            drop_pending_updates=current_webhook.pending_update_count > 0,
        )

        if cfg.debug:
            logger.debug(f"New bot webhook: {await check_webhook(my_bot=my_bot)}")

    except Exception as e:
        logger.error(f"Can't set webhook\nError: {e}")

async def set_commands(my_bot: Bot):
    commands = [
        BotCommand( command="/id", description="👋 Get my ID"),
    ]

    try:
        await my_bot.set_my_commands(commands)
    except Exception as e:
        logger.error(f"Can't set commands - {e}")

async def start_telegram():
    if os.getenv("BOT_FIRST_RUN") == "1":
        return False
    else:
        os.environ["BOT_FIRST_RUN"] = "1"
        await set_webhook(bot)
        await set_commands(bot)
