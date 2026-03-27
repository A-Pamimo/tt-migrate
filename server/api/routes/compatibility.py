"""GET /api/v1/compatibility endpoint."""

from typing import List, Optional

from fastapi import APIRouter, Query

from server.services.compatibility.matrix import (
    get_all_operations,
    lookup_by_category,
    lookup_by_status,
    lookup_operation,
)

router = APIRouter()


@router.get("/compatibility")
async def get_compatibility(
    operation: Optional[str] = Query(
        default=None, description="Specific torch operation to look up"
    ),
    category: Optional[str] = Query(
        default=None, description="Filter by category"
    ),
    status: Optional[str] = Query(
        default=None, description="Filter by status (supported, partial, unsupported)"
    ),
) -> dict:
    """Query the ttnn compatibility matrix.

    Without parameters, returns the full matrix.
    With `operation`, returns a single lookup.
    With `category` or `status`, returns filtered results.
    """
    if operation:
        result = lookup_operation(operation)
        if result is None:
            return {
                "found": False,
                "operation": operation,
                "message": f"Operation '{operation}' not found in the compatibility matrix",
            }
        return {"found": True, "operation": result}

    operations: List[dict] = get_all_operations()

    if category:
        operations = lookup_by_category(category)
    elif status:
        operations = lookup_by_status(status)

    return {
        "total": len(operations),
        "operations": operations,
    }
