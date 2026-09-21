"""Host-level health endpoint."""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    operation_id="get_health",
    description="Report API-process readiness; this does not report worker liveness.",
)
def health() -> dict[str, str]:
    """Report that the API process is ready to receive requests."""
    return {"status": "ok"}
