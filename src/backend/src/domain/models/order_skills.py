from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class OrderSkillsModel(Base):
    __tablename__ = "order_skills"

    # SQL
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.uuid"))
    name: Mapped[str] = mapped_column(String(100))
    icon: Mapped[str | None] = mapped_column(String(200), nullable=True)

    # ORM
    order: Mapped["OrderModel"] = relationship(back_populates="skills")
