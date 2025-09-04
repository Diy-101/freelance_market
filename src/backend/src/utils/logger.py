import logging

from src.settings import get_settings

cfg = get_settings()
logger = logging.getLogger("uvicorn.error")

if cfg.debug:
    logger.setLevel(logging.DEBUG)
