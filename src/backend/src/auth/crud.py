from sqlalchemy.orm import Session
from sqlalchemy import select
from src.auth.models import User
from aiogram.utils.web_app import WebAppUser

def get_user(db: Session, user_id: int) -> User:
    user = db.execute(
        select(User).where(User.tg_id == user_id)
    ).scalar_one_or_none()
    return user

def create_user(db: Session, user_data: WebAppUser) -> User:
    new_user = User(
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
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
