from authx import AuthXConfig
from src.settings import get_settings
from datetime import timedelta

cfg = get_settings()

authx_config = AuthXConfig(
    JWT_SECRET_KEY=cfg.secret_key_jwt,
    JWT_ALGORITHM="HS256",
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=15),  # 30 дней
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=30),
)