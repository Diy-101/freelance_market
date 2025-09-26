from src.proposal_service.services.proposal_service import ProposalService


def get_proposal_service() -> ProposalService:
    return ProposalService()
