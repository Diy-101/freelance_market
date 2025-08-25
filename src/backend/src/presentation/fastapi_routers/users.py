from fastapi import APIRouter, Body, Depends, HTTPException

from src.dependencies import get_user_service
from src.domain.dto import LoginResponse
from src.services import UserService

user_router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)


@user_router.post("/login")
async def login(
    data_string: str = Body(), user_service: UserService = Depends(get_user_service)
) -> LoginResponse:
    try:
        init_data = user_service.check_init_data(data_string)
    except Exception as e:
        raise HTTPException(401, detail=f"Error during initData parsing: {e}")

    new_user = init_data.user
    user = await user_service.get_user(new_user.id)
    if user is None:
        user = await user_service.create_user(new_user)
        token = user_service.create_token(new_user.id)
        return LoginResponse(
            user=user,
            access_token=token,
        )
    user = await user_service.update_user(user.id, new_user)
    if user is None:
        raise HTTPException(404, detail="User not found in database")
    token = user_service.create_token(user.id)
    return LoginResponse(
        user=user,
        access_token=token,
    )
