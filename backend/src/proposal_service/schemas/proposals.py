from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ProposalBase(BaseModel):
    order_id: str
    freelancer_id: int
    message: str
    price: int  # Price in kopecks


class ProposalCreate(ProposalBase):
    pass


class ProposalUpdate(BaseModel):
    message: Optional[str] = None
    price: Optional[int] = None
    status: Optional[str] = None


class Proposal(ProposalBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
