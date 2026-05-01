from typing import Any

from fastapi import APIRouter

from app.api.deps import ManagerOrAdminDep

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get(
    "/",
    dependencies=[ManagerOrAdminDep],
)
def read_metrics() -> Any:
    """
    Retrieve application metrics.
    Accessible by Admin and Manager roles.
    This is a stub endpoint — extend with real metrics as needed.
    """
    return {
        "total_users": 0,
        "active_users": 0,
        "total_items": 0,
        "notes": "Metrics endpoint stub — integrate with your data layer for real values.",
    }
