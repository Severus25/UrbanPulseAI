"""Unit tests for LangGraph Orchestration Service & Agents."""

import pytest
from httpx import AsyncClient, ASGITransport
from services.orchestration.app.main import app
from agents.graph import LocalDocumentRetriever, create_urbanpulse_graph


@pytest.mark.asyncio
async def test_health_check():
    """Verify that the orchestration health endpoint is functional."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "orchestration"}


@pytest.mark.asyncio
async def test_local_document_retriever():
    """Verify that the pure-python RAG retriever can search municipal files."""
    retriever = LocalDocumentRetriever()
    
    # Test retrieving weather advisory
    results = retriever.retrieve("flooding rainfall advisory 204", top_k=1)
    assert len(results) > 0
    assert "advisory_204_weather_restrictions.md" in results[0]["source"]
    assert "Speed Reductions" in results[0]["content"]

    # Test retrieving stadium advisory
    results = retriever.retrieve("stadium event special bypass", top_k=1)
    assert len(results) > 0
    assert "advisory_305_stadium_events.md" in results[0]["source"]


@pytest.mark.asyncio
async def test_process_query_traffic():
    """Verify routing and data collection for congestion queries."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {"query": "Tell me about congestion on Broadway Corridor"}
        response = await client.post("/api/v1/query", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert "Broadway" in data["explanation"] or "congestion" in data["explanation"].lower()
    assert "traffic_reasoner_agent" in data["agents_used"]
    assert "traffic_data" in data["data"]
    assert "incident_data" in data["data"]
    assert data["data"]["traffic_data"]["congestion_index"] == 0.55


@pytest.mark.asyncio
async def test_process_query_route_under_rain():
    """Verify that heavy rainfall triggers appropriate flood detours."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {"query": "What is the best route bypass due to heavy rain?"}
        response = await client.post("/api/v1/query", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert len(data["recommendations"]) > 0
    assert any("River Valley Road" in rec for rec in data["recommendations"])
    assert any("Elevated Bypass" in rec for rec in data["recommendations"])
    assert "mobility_planner_agent" in data["agents_used"]


@pytest.mark.asyncio
async def test_process_query_policy_rag():
    """Verify RAG retrieval integration inside query loop."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {"query": "What is speed limit regulation under Advisory 204?"}
        response = await client.post("/api/v1/query", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "retrieved_docs" in data["data"]
    assert len(data["data"]["retrieved_docs"]) > 0
    assert "advisory_204" in data["data"]["retrieved_docs"][0]["source"]
    assert "policy_retrieval_agent" in data["agents_used"]


@pytest.mark.asyncio
async def test_process_query_simulate():
    """Verify that what-if simulation requests invoke simulation agent."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "query": "What if we close Arena Way segment 102?",
            "location": None
        }
        response = await client.post("/api/v1/query", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "simulation_agent" in data["agents_used"]
    assert "simulation_result" in data["data"]
    assert data["data"]["simulation_result"]["system_delay_increase_seconds"] == 450


@pytest.mark.asyncio
async def test_simulation_endpoint():
    """Verify direct simulation endpoint returns impact stats."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {"query": "Simulate Arena Way closure"}
        response = await client.post("/api/v1/simulate", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert "impact" in data
    assert "Broadway Corridor" in str(data["impact"]["downstream_impact"])
