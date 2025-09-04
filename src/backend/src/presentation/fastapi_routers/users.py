from fastapi import APIRouter, Body, Depends, HTTPException, status

from src.application.services import TelegramService, UserService
from src.dependencies import get_telegram_service, get_user_service
from src.presentation.dto import LoginResponse
from src.settings import get_settings
from src.utils import logger

cfg = get_settings()

user_router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)


@user_router.post("/login")
async def login(
    data_string: str = Body(embed=True),
    user_service: UserService = Depends(get_user_service),
    telegram_service: TelegramService = Depends(get_telegram_service),
) -> LoginResponse:
    if cfg.debug:
        logger.debug(data_string)

    # Validating initData from Telegram API
    try:
        init_data = telegram_service.validate_init_data(data_string)
    except Exception as e:
        raise HTTPException(401, detail=f"Error during initData parsing: {e}")

    # Check the user existence
    user_dict = init_data["user"]
    is_user_exist = (
        True if await user_service.get_user_by_tg_id(user_dict["tg_id"]) else False
    )

    # Creates a new user
    if not is_user_exist:
        user = await user_service.create_user(user_dict)
        try:
            token = user_service.create_token(user.tg_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Impossible to create an access token: {e}",
            )
    # Update the user that exists
    else:
        user = await user_service.update_user_by_tg_id(
            int(user_dict["tg_id"]), user_dict
        )
        try:
            token = user_service.create_token(user.tg_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Impossible to create an access token: {e}",
            )

    # Form a response body
    response = LoginResponse(
        user=user,
        access_token=token,
    )

    if cfg.debug:
        logger.debug(f"Response: {response}")

    return response
