from pydantic import BaseModel
from src.domain.schemas.users import User


class Order(BaseModel):
    id: int
    title: str
    author: User

