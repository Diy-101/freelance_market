from typing import Any
from sqlalchemy import select, insert

from src.database import SessionLocal
from src.auth.models import UserModel


async def get_user(user_id: int) -> UserModel:
    async with SessionLocal() as session:
        user = await session.execute(
            select(UserModel).where(UserModel.tg_id == user_id)
        )
        user = user.scalar_one_or_none()
        return user


async def create_user(user_data: dict[str, Any]) -> UserModel:
    async with SessionLocal() as session:
        new_user = UserModel(
            tg_id=user_data["id"],
            is_bot=user_data["is_bot"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            username=user_data["username"],
            language_code=user_data["language_code"],
            is_premium=user_data["is_premium"],
            added_to_attachment_menu=user_data["added_to_attachment_menu"],
            allows_write_to_pm=user_data["allows_write_to_pm"],
            photo_url=user_data["photo_url"],
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user


async def update_user(new_data: dict, user_model: UserModel) -> UserModel:
    async with SessionLocal() as session:
        for field, value in new_data.items():
            if hasattr(user_model, field):
                setattr(user_model, field, value)
        session.commit()
        session.refresh(user_model)
        return user_model
