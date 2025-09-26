from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class SkillModel(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True, unique=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[str] = mapped_column(String(500))
    category: Mapped[str] = mapped_column(String(50), index=True)
