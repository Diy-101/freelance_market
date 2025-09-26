from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional

from src.search_service.schemas.search import SearchResponse, SearchFilters
from src.search_service.services.search_service import SearchService
from src.dependencies import get_search_service

search_router = APIRouter(
    prefix="/api/search",
    tags=["search"],
)


@search_router.get("/orders", response_model=SearchResponse)
async def search_orders(
    query: Optional[str] = Query(None, description="Search query"),
    category: Optional[str] = Query(None, description="Category filter"),
    min_price: Optional[int] = Query(None, description="Minimum price in kopecks"),
    max_price: Optional[int] = Query(None, description="Maximum price in kopecks"),
    skills: Optional[str] = Query(None, description="Comma-separated skills"),
    status: Optional[str] = Query(None, description="Order status"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    search_service: SearchService = Depends(get_search_service),
) -> SearchResponse:
    """Search orders with filters"""
    try:
        filters = SearchFilters(
            query=query,
            category=category,
            min_price=min_price,
            max_price=max_price,
            skills=skills.split(",") if skills else None,
            status=status,
            page=page,
            limit=limit
        )
        return await search_service.search_orders(filters)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Search failed: {e}",
        )


@search_router.get("/freelancers", response_model=SearchResponse)
async def search_freelancers(
    query: Optional[str] = Query(None, description="Search query"),
    skills: Optional[str] = Query(None, description="Comma-separated skills"),
    rating_min: Optional[float] = Query(None, ge=0, le=5, description="Minimum rating"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    search_service: SearchService = Depends(get_search_service),
) -> SearchResponse:
    """Search freelancers with filters"""
    try:
        filters = SearchFilters(
            query=query,
            skills=skills.split(",") if skills else None,
            rating_min=rating_min,
            page=page,
            limit=limit
        )
        return await search_service.search_freelancers(filters)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Search failed: {e}",
        )


@search_router.get("/suggestions")
async def get_search_suggestions(
    query: str = Query(..., description="Search query"),
    type: str = Query("all", description="Type: orders, freelancers, skills, all"),
    search_service: SearchService = Depends(get_search_service),
) -> dict:
    """Get search suggestions"""
    try:
        return await search_service.get_suggestions(query, type)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to get suggestions: {e}",
        )
