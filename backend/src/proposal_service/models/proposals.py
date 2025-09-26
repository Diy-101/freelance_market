from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class ProposalModel(Base):
    __tablename__ = "proposals"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    order_id: Mapped[str] = mapped_column(ForeignKey("orders.uuid"))
    freelancer_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"))
    message: Mapped[str] = mapped_column(Text)
    price: Mapped[int] = mapped_column(Integer)  # Price in kopecks
    status: Mapped[str] = mapped_column(String(20), default="pending")  # pending, accepted, rejected
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=func.now())

    # ORM
    order: Mapped["OrderModel"] = relationship(back_populates="proposals")
    freelancer: Mapped["UserModel"] = relationship(back_populates="proposals")
