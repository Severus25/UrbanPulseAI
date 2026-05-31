from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/current")
async def get_current_weather(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
):
    """Get current weather conditions."""
    # TODO: Call OpenWeatherMap API or cached data
    return {
        "location": {"lat": lat, "lon": lon},
        "temperature_c": None,
        "humidity_pct": None,
        "precipitation_mm": None,
        "visibility_km": None,
        "wind_speed_kmh": None,
        "condition": "unknown",
    }


@router.get("/forecast")
async def get_weather_forecast(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
    hours: int = Query(24, description="Forecast horizon in hours"),
):
    """Get weather forecast."""
    return {"location": {"lat": lat, "lon": lon}, "hours": hours, "forecast": []}


@router.get("/alerts")
async def get_weather_alerts(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude"),
):
    """Get active weather alerts for an area."""
    return {"alerts": []}
