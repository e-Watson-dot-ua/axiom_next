from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status

from app.api.deps import include_deleted, search_query
from app.models.division import Division
from app.schemas.division import DivisionCreate, DivisionUpdate
from app.services.division import get_division_service, DivisionService

router = APIRouter(tags = ["divisions"])


@router.get("/", response_model = List[Division])
async def get_divisions(
    skip: int = Query(0, ge = 0, description = "Records to skip"),
    limit: int = Query(20, ge = 1, le = 100, description = "Records per page"),
    include_deleted: bool = Depends(include_deleted),
    search: Optional[str] = Depends(search_query),
    active_only: bool = Query(True, description = "Show only active records"),
    service: DivisionService = Depends(get_division_service)
):
    # Get list of divisions with pagination and filtering
    return service.get_all(
        skip = skip,
        limit = limit,
        include_deleted = include_deleted,
        search = search,
        active_only = active_only
    )


@router.get("/list", response_model = List[Division])
async def get_divisions_list(
    include_deleted: bool = Depends(include_deleted),
    search: Optional[str] = Depends(search_query),
    active_only: bool = Query(True, description = "Show only active records"),
    service: DivisionService = Depends(get_division_service)
):
    # Get all divisions without pagination (for dropdowns, etc.)
    return service.get_list(
        include_deleted = include_deleted,
        search = search,
        active_only = active_only
    )


@router.get("/{division_id}", response_model = Division)
async def get_division(
    division_id: int,
    include_deleted: bool = Depends(include_deleted),
    service: DivisionService = Depends(get_division_service)
):
    # Get division by ID
    return service.get_by_id(division_id, include_deleted = include_deleted)


@router.get("/by-code/{code}", response_model = Division)
async def get_division_by_code(
    code: str,
    include_deleted: bool = Depends(include_deleted),
    service: DivisionService = Depends(get_division_service)
):
    # Get division by code
    return service.get_by_code(code, include_deleted = include_deleted)


@router.post("/", response_model = Division, status_code = status.HTTP_201_CREATED)
async def create_division(
    division_data: DivisionCreate,
    service: DivisionService = Depends(get_division_service)
):
    # Create new division
    return service.create(division_data)


@router.put("/{division_id}", response_model = Division)
async def update_division(
    division_id: int,
    update_data: DivisionUpdate,
    service: DivisionService = Depends(get_division_service)
):
    # Update division by ID
    return service.update(division_id, update_data)


@router.patch("/{division_id}", response_model = Division)
async def patch_division(
    division_id: int,
    update_data: DivisionUpdate,
    service: DivisionService = Depends(get_division_service)
):
    # Partially update division by ID
    return service.update(division_id, update_data)


@router.delete("/{division_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_division(
    division_id: int,
    soft_delete: bool = Query(True, description = "Use soft delete (mark as deleted)"),
    service: DivisionService = Depends(get_division_service)
):
    # Delete division by ID
    service.delete(division_id, soft_delete = soft_delete)


@router.post("/{division_id}/restore", response_model = Division)
async def restore_division(
    division_id: int,
    service: DivisionService = Depends(get_division_service)
):
    # Restore soft-deleted division
    return service.restore(division_id)


# Hierarchical operations
@router.get("/{division_id}/children", response_model = List[Division])
async def get_division_children(
    division_id: int,
    include_deleted: bool = Depends(include_deleted),
    service: DivisionService = Depends(get_division_service)
):
    # Get child divisions of a parent division
    # Verify parent exists first
    service.get_by_id(division_id, include_deleted = include_deleted)
    return service.get_children(division_id, include_deleted = include_deleted)


@router.get("/hierarchy/tree", response_model = List[Division])
async def get_division_hierarchy(
    root_id: Optional[int] = Query(None, description = "Root division ID (null for top level)"),
    service: DivisionService = Depends(get_division_service)
):
    # Get division hierarchy tree
    return service.get_hierarchy_tree(root_id)


@router.put("/{division_id}/move", response_model = Division)
async def move_division(
    division_id: int,
    new_parent_id: Optional[int] = Query(None, description = "New parent ID (null for root)"),
    new_sort_order: Optional[int] = Query(None, description = "New sort order"),
    service: DivisionService = Depends(get_division_service)
):
    # Move division to new parent with optional sort order
    return service.move_division(division_id, new_parent_id, new_sort_order)


# Utility endpoints
@router.get("/codes/available", response_model = List[str])
async def get_available_codes(
    prefix: Optional[str] = Query(None, description = "Code prefix filter"),
    service: DivisionService = Depends(get_division_service)
):
    # Get list of available division codes
    return service.get_available_codes(prefix = prefix)


@router.get("/search/suggest", response_model = List[Division])
async def search_divisions_suggest(
    q: str = Query(..., min_length = 2, description = "Search query (minimum 2 characters)"),
    limit: int = Query(10, ge = 1, le = 50, description = "Maximum suggestions"),
    service: DivisionService = Depends(get_division_service)
):
    # Search divisions with suggestions (for autocomplete)
    return service.get_all(
        skip = 0,
        limit = limit,
        search = q,
        active_only = True,
        include_deleted = False
    )
