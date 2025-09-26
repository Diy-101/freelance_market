from datetime import datetime
from typing import List, Optional

from src.proposal_service.models.proposals import ProposalModel
from src.proposal_service.schemas.proposals import (
    Proposal,
    ProposalCreate,
    ProposalUpdate,
)
from src.repository import get_repository


class ProposalService:
    """Service for managing proposals"""

    def __init__(self):
        self._repository = get_repository(ProposalModel, Proposal, "id")

    async def create_proposal(self, proposal_data: ProposalCreate) -> Proposal:
        """Create a new proposal"""
        proposal = Proposal(
            id=0,  # Will be set by database
            order_id=proposal_data.order_id,
            freelancer_id=proposal_data.freelancer_id,
            message=proposal_data.message,
            price=proposal_data.price,
            status="pending",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        proposal_id = await self._repository.create(proposal)
        return await self.get_proposal_by_id(proposal_id)

    async def get_proposals(
        self, order_id: Optional[str] = None, freelancer_id: Optional[int] = None
    ) -> List[Proposal]:
        """Get proposals, optionally filtered by order or freelancer"""
        proposals = await self._repository.get_all()
        if order_id:
            proposals = [p for p in proposals if p.order_id == order_id]
        if freelancer_id:
            proposals = [p for p in proposals if p.freelancer_id == freelancer_id]
        return proposals

    async def get_proposal_by_id(self, proposal_id: int) -> Optional[Proposal]:
        """Get proposal by ID"""
        return await self._repository.get_by_id(proposal_id)

    async def update_proposal(
        self, proposal_id: int, proposal_data: ProposalUpdate
    ) -> Proposal:
        """Update proposal by ID"""
        values = {k: v for k, v in proposal_data.model_dump().items() if v is not None}
        values["updated_at"] = datetime.now()
        return await self._repository.update(proposal_id, values)

    async def delete_proposal(self, proposal_id: int) -> None:
        """Delete proposal by ID"""
        await self._repository.delete(proposal_id)

    async def accept_proposal(self, proposal_id: int) -> None:
        """Accept a proposal"""
        await self.update_proposal(proposal_id, ProposalUpdate(status="accepted"))

    async def reject_proposal(self, proposal_id: int) -> None:
        """Reject a proposal"""
        await self.update_proposal(proposal_id, ProposalUpdate(status="rejected"))
