"""Tests for Data Gateway health endpoint."""

import pytest
from httpx import AsyncClient, ASGITransport
from services.data_gateway.app.main import app


@pytest.mark.asyncio
async def test_health_check():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_traffic_current():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/v1/traffic/current?lat=40.73&lon=-73.93")
    assert response.status_code == 200
    data = response.json()
    assert "center" in data
    assert "segments" in data
