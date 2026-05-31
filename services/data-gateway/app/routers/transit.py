from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/delays")
async def get_transit_delays(
    route_id: str | None = Query(None, description="Filter by route ID"),
):
    """Get current transit delays."""
    return {"delays": [], "route_id": route_id}


@router.get("/routes")
async def get_transit_routes():
    """Get available transit routes."""
    return {"routes": []}


@router.get("/predictions")
async def get_delay_predictions(
    route_id: str = Query(..., description="Route ID"),
    stop_id: str = Query(..., description="Stop ID"),
):
    """Predict transit delays for a specific route/stop."""
    return {"route_id": route_id, "stop_id": stop_id, "predicted_delay_minutes": 0}
