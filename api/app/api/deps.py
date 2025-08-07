from typing import Optional, Generator
from fastapi import Depends, Query
from sqlmodel import Session

from app.core.database import get_db_session


# Database session dependency
def get_db() -> Generator[Session, None, None]:
    # Database session dependency for API endpoints
    yield from get_db_session()


# Pagination parameters
class PaginationParams:
    def __init__(
        self,
        skip: int = Query(0, ge=0, description="Records to skip"),
        limit: int = Query(20, ge=1, le=100, description="Records per page")
    ):
        self.skip = skip
        self.limit = limit


# Common query parameters
def get_pagination() -> PaginationParams:
    # Pagination parameters for list endpoints
    return Depends(PaginationParams)


# Filter parameters
def include_deleted(
    include_deleted: bool = Query(False, description="Include soft-deleted records")
) -> bool:
    # Whether to include soft-deleted records
    return include_deleted


# Search parameters
def search_query(
    q: Optional[str] = Query(None, description="Search query")
) -> Optional[str]:
    # Search query parameter
    return q


# Sort parameters
def sort_params(
    sort_by: Optional[str] = Query(None, description="Sort field"),
    sort_order: str = Query("asc", regex="^(asc|desc)$", description="Sort order")
) -> tuple[Optional[str], str]:
    # Sort parameters for list endpoints
    return sort_by, sort_order


# Active records filter
def active_only(
    active_only: bool = Query(True, description="Show only active records")
) -> bool:
    # Filter for active vs all records
    return active_only


# Date range parameters
def date_range_params(
    date_from: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
) -> tuple[Optional[str], Optional[str]]:
    # Date range filtering for reports
    return date_from, date_to
