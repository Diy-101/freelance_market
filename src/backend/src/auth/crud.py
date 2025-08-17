from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from src.auth.models import UserModel
from src.auth.schemas import UserSchema

async def get_user(session: AsyncSession, user_id: int) -> UserModel:
    user = await session.execute(
        select(UserModel).where(UserModel.tg_id == user_id)
    )
    user = user.scalar_one_or_none()
    return user

async def create_user(session: AsyncSession, user_data: UserSchema) -> UserSchema:
    new_user = UserModel(
        tg_id=user_data.id,
        is_bot=user_data.is_bot,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        username=user_data.username,
        language_code=user_data.language_code,
        is_premium=user_data.is_premium,
        added_to_attachment_menu=user_data.added_to_attachment_menu,
        allows_write_to_pm=user_data.allows_write_to_pm,
        photo_url=user_data.photo_url,
    )
    stmt = insert(UserModel).values([new_user])
    await session.execute(stmt)
    await session.commit()
    await session.refresh(new_user)
    return user_data
