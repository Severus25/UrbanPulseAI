from fastapi import APIRouter, Query
from datetime import datetime

router = APIRouter()


@router.get("/active")
async def get_active_incidents(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    radius_km: float = Query(10.0, description="Radius in km"),
):
    """Get active road incidents in an area."""
    return {
        "center": {"lat": lat, "lon": lon},
        "radius_km": radius_km,
        "incidents": [],
    }


@router.get("/history")
async def get_incident_history(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    days: int = Query(30, description="Lookback days"),
):
    """Get historical incidents for risk analysis."""
    return {"incidents": [], "period_days": days}


@router.get("/risk")
async def get_risk_score(
    segment_id: str = Query(..., description="Road segment ID"),
):
    """Get accident/disruption risk score for a road segment."""
    return {
        "segment_id": segment_id,
        "risk_score": 0.0,
        "risk_factors": [],
        "timestamp": datetime.utcnow().isoformat(),
    }
