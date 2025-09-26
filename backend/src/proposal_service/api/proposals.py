from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from src.proposal_service.schemas.proposals import Proposal, ProposalCreate, ProposalUpdate
from src.proposal_service.services.proposal_service import ProposalService
from src.dependencies import get_proposal_service

proposal_router = APIRouter(
    prefix="/api/proposals",
    tags=["proposals"],
)


@proposal_router.post("/", response_model=Proposal)
async def create_proposal(
    proposal_data: ProposalCreate,
    proposal_service: ProposalService = Depends(get_proposal_service),
) -> Proposal:
    """Create a new proposal"""
    try:
        return await proposal_service.create_proposal(proposal_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create proposal: {e}",
        )


@proposal_router.get("/", response_model=List[Proposal])
async def get_proposals(
    order_id: str = None,
    freelancer_id: int = None,
    proposal_service: ProposalService = Depends(get_proposal_service),
) -> List[Proposal]:
    """Get proposals, optionally filtered by order or freelancer"""
    return await proposal_service.get_proposals(order_id, freelancer_id)


@proposal_router.get("/{proposal_id}", response_model=Proposal)
async def get_proposal(
    proposal_id: int,
    proposal_service: ProposalService = Depends(get_proposal_service),
) -> Proposal:
    """Get proposal by ID"""
    proposal = await proposal_service.get_proposal_by_id(proposal_id)
    if proposal is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proposal not found",
        )
    return proposal


@proposal_router.put("/{proposal_id}", response_model=Proposal)
async def update_proposal(
    proposal_id: int,
    proposal_data: ProposalUpdate,
    proposal_service: ProposalService = Depends(get_proposal_service),
) -> Proposal:
    """Update proposal by ID"""
    try:
        return await proposal_service.update_proposal(proposal_id, proposal_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update proposal: {e}",
        )


@proposal_router.delete("/{proposal_id}")
async def delete_proposal(
    proposal_id: int,
    proposal_service: ProposalService = Depends(get_proposal_service),
) -> dict:
    """Delete proposal by ID"""
    try:
        await proposal_service.delete_proposal(proposal_id)
        return {"message": "Proposal deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to delete proposal: {e}",
        )


@proposal_router.post("/{proposal_id}/accept")
async def accept_proposal(
    proposal_id: int,
    proposal_service: ProposalService = Depends(get_proposal_service),
) -> dict:
    """Accept a proposal"""
    try:
        await proposal_service.accept_proposal(proposal_id)
        return {"message": "Proposal accepted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to accept proposal: {e}",
        )


@proposal_router.post("/{proposal_id}/reject")
async def reject_proposal(
    proposal_id: int,
    proposal_service: ProposalService = Depends(get_proposal_service),
) -> dict:
    """Reject a proposal"""
    try:
        await proposal_service.reject_proposal(proposal_id)
        return {"message": "Proposal rejected successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to reject proposal: {e}",
        )
