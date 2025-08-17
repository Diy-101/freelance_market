from fastapi import APIRouter, Depends, HTTPException
from aiogram.utils.web_app import safe_parse_webapp_init_data

from src.settings import get_settings, Settings
from src.auth import authx
from src.auth.crud import get_user, create_user, update_user
from src.auth.schemas import InitDataSchema, LoginSchema, UserSchema
from src.utils.logger import logger

user_router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
)


@user_router.post("/login")
async def validate_user(
    data: InitDataSchema,
    cfg: Settings = Depends(get_settings),
) -> LoginSchema:
    try:
        # Check signature
        init_data = safe_parse_webapp_init_data(
            token=cfg.bot_token, init_data=data.init_data
        )
    except Exception as err:
        raise HTTPException(status_code=400, detail=f"Invalid initData: {err}")
    user_data = init_data.user.model_dump()

    # Добавление пользователя в БД
    user_model = await get_user(user_data['id'])
    if user_model is None:
        await create_user(user_data)
    else:
        # Изменение данных, если они изменились в TG
        current_data = UserSchema(**user_model.__dict__).model_dump()
        if current_data != user_data:
            if cfg.debug:
                logger.info("User data differs from current data")
            await update_user(user_data, user_model)

    # Создание токена по id
    access_token = authx.create_access_token(uid=str(user_data["id"]))
    return LoginSchema(
        user=UserSchema(**user_data),
        access_token=access_token,
    )
