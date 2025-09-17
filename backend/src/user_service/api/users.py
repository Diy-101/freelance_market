from fastapi import APIRouter, Body, Depends, HTTPException, Path
from src.settings import get_settings
from src.user_service.dependencies import get_main_service
from src.user_service.schemas.users import LoginResponse, User
from src.user_service.services import MainUserService
from src.utils import logger

cfg = get_settings()

user_router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)


@user_router.post("/")
async def create_user(
    user: User = Body(...),
    main_service: MainUserService = Depends(get_main_service),
) -> User:
    return await main_service.create_user(user)


@user_router.get("/", response_model=list[User])
async def get_all_users(
    main_service: MainUserService = Depends(get_main_service),
) -> list[User]:
    return await main_service.get_all_users()


@user_router.get("/{tg_id}", response_model=User)
async def get_user(
    tg_id: int = Path(..., description="Telegram ID of the user"),
    main_service: MainUserService = Depends(get_main_service),
) -> User:
    user = await main_service.get_user(tg_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.put("/{tg_id}", response_model=User)
async def update_user(
    tg_id: int = Path(..., description="Telegram ID of the user"),
    user: User = Body(...),
    main_service: MainUserService = Depends(get_main_service),
) -> User:
    return await main_service.update_user(tg_id, user)


@user_router.delete("/{tg_id}", response_model=User)
async def delete_user(
    tg_id: int = Path(..., description="Telegram ID of the user"),
    main_service: MainUserService = Depends(get_main_service),
) -> User:
    return await main_service.delete_user(tg_id)


@user_router.post("/login")
async def login(
    init_data: str = Body(..., embed=True),
    main_service: MainUserService = Depends(get_main_service),
) -> LoginResponse:
    logger.info(f"InitData: {init_data}")
    return await main_service.login_user(init_data=init_data)
