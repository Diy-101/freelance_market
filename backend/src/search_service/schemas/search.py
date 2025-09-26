from typing import List, Optional, Any, Dict
from pydantic import BaseModel


class SearchFilters(BaseModel):
    query: Optional[str] = None
    category: Optional[str] = None
    min_price: Optional[int] = None
    max_price: Optional[int] = None
    skills: Optional[List[str]] = None
    status: Optional[str] = None
    rating_min: Optional[float] = None
    page: int = 1
    limit: int = 20


class SearchResponse(BaseModel):
    items: List[Dict[str, Any]]
    total: int
    page: int
    limit: int
    total_pages: int
