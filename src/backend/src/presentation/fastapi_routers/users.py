from fastapi import APIRouter, Body, Depends, HTTPException, status

from src.application.services import TelegramService, UserService
from src.dependencies import get_telegram_service, get_user_service
from src.presentation.dto import LoginResponse

user_router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)


@user_router.post("/login")
async def login(
    data_string: str = Body(embed=False),
    user_service: UserService = Depends(get_user_service),
    telegram_service: TelegramService = Depends(get_telegram_service),
) -> LoginResponse:
    try:
        init_data = telegram_service.validate_init_data(data_string)
    except Exception as e:
        raise HTTPException(401, detail=f"Error during initData parsing: {e}")

    user = init_data.user
    is_user_exist = True if await user_service.get_user_by_tg_id(user.tg_id) else False

    if not is_user_exist:
        user = await user_service.create_user(user)
        try:
            token = user_service.create_token(user.tg_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Impossible to create an access token: {e}",
            )

        return LoginResponse(
            user=user,
            access_token=token,
        )
    else:
        user = await user_service.update_user_by_tg_id(int(user.tg_id), user)
        try:
            token = user_service.create_token(user.tg_id)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Impossible to create an access token: {e}",
            )

        return LoginResponse(
            user=user,
            access_token=token,
        )
