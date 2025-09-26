from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class NotificationModel(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"))
    title: Mapped[str] = mapped_column(String(200))
    message: Mapped[str] = mapped_column(Text)
    type: Mapped[str] = mapped_column(String(50))  # order, proposal, message, system
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # ORM
    user: Mapped["UserModel"] = relationship(back_populates="notifications")
