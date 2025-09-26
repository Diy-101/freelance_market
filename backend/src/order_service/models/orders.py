from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base
from src.order_service.schemas.orders import OrderStatus


class OrderModel(Base):
    __tablename__ = "orders"

    # SQL
    uuid: Mapped[str] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    author_id: Mapped[str] = mapped_column(ForeignKey("users.uuid"))
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus))
    primary_responses: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=func.now())

    # ORM
    author: Mapped["UserModel"] = relationship(back_populates="orders")
    skills: Mapped[list["OrderSkillsModel"]] = relationship(back_populates="order")
    proposals: Mapped[list["ProposalModel"]] = relationship(back_populates="order")
