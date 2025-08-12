from fastapi import APIRouter, Request, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from aiogram.utils.web_app import safe_parse_webapp_init_data, WebAppInitData, WebAppUser

from src.settings import get_settings, Settings
from src.utils.database import get_db
from src.auth.models import User
from src.auth import authx
from src.auth.schemas import SignIn, InitData
from src.utils.logger import logger

user_router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
)

@user_router.post("/signin")
async def signin(
        data: InitData,
        cfg: Settings = Depends(get_settings),
        db: Session = Depends(get_db)
):
    try:
        # Проверка подписи
        logger.info("RAW init_data:", data.init_data)
        init_data = safe_parse_webapp_init_data(token=cfg.bot_token, init_data=data.init_data)
        user_data = init_data.user
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Invalid initData: {err}")


    user = db.execute(select(User).where(User.tg_id == user_data.id)).scalar_one_or_none()
    if not user:
        new_user = User(**user_data.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    access_token = authx.create_access_token(uid=user_data.id)
    refresh_token = authx.create_refresh_token(uid=user_data.id)

    return SignIn(
        access_token=access_token,
        refresh_token=refresh_token,
        user=user_data
    )



