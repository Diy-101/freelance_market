from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import instance_dict
from aiogram.utils.web_app import safe_parse_webapp_init_data

from src.settings import get_settings, Settings
from src.utils.database import get_db
from src.auth import authx
from src.auth.schemas import SignIn, InitData
from src.auth.crud import get_user, create_user

user_router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
)


@user_router.post("/signin")
async def validate_user(
    data: InitData,
    cfg: Settings = Depends(get_settings),
    db: Session = Depends(get_db),
) -> SignIn:
    try:
        # Проверка подписи
        init_data = safe_parse_webapp_init_data(
            token=cfg.bot_token, init_data=data.init_data
        )
        user_data = init_data.user
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Invalid initData: {err}")

    # Добавление пользователя в БД
    user = get_user(db, user_data.id)
    if user is None:
        create_user(db, user_data)
    else:
        # Изменение данных, если они изменились в TG
        db_data = instance_dict(user)
        user_data_dict = user_data.model_dump()
        filtered_db_data = {k: db_data[k] for k in user_data_dict.keys()}
        if user_data_dict != filtered_db_data:
            for field, value in user_data_dict.items():
                if hasattr(user, field):
                    setattr(user, field, value)
            db.commit()

    access_token = authx.create_access_token(uid=int(user_data.id))
    return SignIn(
        user=user_data,
        access_token=access_token,
    )
