from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    tg_id: Mapped[int] = mapped_column(unique=True, index=True, nullable=False)
    is_bot: Mapped[bool | None] = None
    first_name: Mapped[str]
    last_name: Mapped[str | None] = None
    username: Mapped[str | None] = None
    language_code: Mapped[str | None] = None
    is_premium: Mapped[bool | None] = None
    added_to_attachment_menu: Mapped[bool | None] = None
    allows_write_to_pm: Mapped[bool | None] = None
    photo_url: Mapped[str | None] = None

