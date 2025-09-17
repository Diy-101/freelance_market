from typing import Optional

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base


class UserModel(Base):
    __tablename__ = "users"

    # SQL
    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(unique=True, index=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(200))
    last_name: Mapped[Optional[str]] = mapped_column(String(200))
    username: Mapped[Optional[str]] = mapped_column(String(200))
    language_code: Mapped[Optional[str]] = mapped_column(String(2))
    is_premium: Mapped[Optional[bool]] = mapped_column(Boolean)
    allows_write_to_pm: Mapped[Optional[bool]] = mapped_column(Boolean)
    photo_url: Mapped[Optional[str]] = mapped_column(String(200))

    # ORM
    skills: Mapped[list["UserSkillsModel"]] = relationship(back_populates="user")
