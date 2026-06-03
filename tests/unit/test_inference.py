"""Unit tests for the FastAPI ML Inference Service."""

import pytest
from httpx import AsyncClient, ASGITransport
from services.inference.app.main import app


@pytest.mark.asyncio
async def test_health_check():
    """Verify the inference health endpoint is responsive."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "inference"}


@pytest.mark.asyncio
async def test_list_models():
    """Verify that all serving and stub models are correctly listed."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/models")
    assert response.status_code == 200
    data = response.json()
    assert "models" in data
    assert len(data["models"]) > 0
    names = [model["name"] for model in data["models"]]
    assert "congestion_xgboost" in names
    assert "risk_scorer" in names


@pytest.mark.asyncio
async def test_predict_congestion():
    """Verify that predictions are generated for the congestion forecasting model."""
    transport = ASGITransport(app=app)
    payload = {
        "model_name": "congestion",
        "segment_id": "seg_broadway_42",
        "features": {
            "hour_of_day": 8,
            "day_of_week": 1,
            "is_weekend": 0,
            "is_holiday": 0,
            "segment_length_m": 250.0,
            "num_lanes": 3,
            "speed_limit_kmh": 50.0,
            "historical_avg_speed": 42.0,
            "historical_std_speed": 8.0,
            "lag_1h_speed": 35.0,
            "lag_2h_speed": 38.0,
            "lag_24h_speed": 40.0,
            "weather_temp_c": 12.0,
            "weather_precip_mm": 5.0,
            "weather_visibility_km": 8.0,
            "nearby_events_count": 0,
            "upstream_congestion": 0.2,
        },
    }

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/predict", json=payload)
    
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["model_name"] == "congestion"
    assert "predicted_speed_kmh" in res_data["prediction"]
    assert "congestion_level" in res_data["prediction"]
    assert "contributing_factors" in res_data["prediction"]
    assert res_data["confidence"] > 0.0
    assert "shap_values" in res_data["explanation"]


@pytest.mark.asyncio
async def test_predict_risk():
    """Verify that disruption risk score predictions are calculated and structured correctly."""
    transport = ASGITransport(app=app)
    payload = {
        "model_name": "risk",
        "segment_id": "seg_lowland_5",
        "features": {
            "weather": {
                "precipitation_mm": 20.0,
                "temperature_c": 5.0,
            },
            "events": [
                {
                    "expected_attendance": 45000,
                    "distance_km": 0.5,
                }
            ],
            "incident_history": [
                {"severity": "major"},
                {"severity": "minor"},
            ],
            "current_traffic": {
                "current_speed": 15.0,
                "free_flow_speed": 50.0,
            },
        },
    }

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/predict", json=payload)
        
    assert response.status_code == 200
    res_data = response.json()
    assert res_data["model_name"] == "risk"
    
    pred = res_data["prediction"]
    assert "overall_risk" in pred
    assert "flooding_risk" in pred
    assert "accident_risk" in pred
    assert "recommended_actions" in pred
    assert len(pred["contributing_factors"]) > 0
    assert len(pred["recommended_actions"]) > 0


@pytest.mark.asyncio
async def test_predict_unsupported_model():
    """Verify fallback stub response behavior for unsupported models."""
    transport = ASGITransport(app=app)
    payload = {
        "model_name": "unsupported_model_stub",
        "features": {},
    }

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/predict", json=payload)

    assert response.status_code == 200
    res_data = response.json()
    assert res_data["model_name"] == "unsupported_model_stub"
    assert "status" in res_data["prediction"]
    assert res_data["prediction"]["status"] == "stub_not_implemented"
