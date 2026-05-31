"""UrbanPulse AI - Orchestration Service (Agent Gateway)"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

app = FastAPI(title="UrbanPulse AI - Orchestration Service", version="0.1.0")


class QueryRequest(BaseModel):
    query: str
    location: dict | None = None
    context: dict = {}


class QueryResponse(BaseModel):
    query: str
    explanation: str
    recommendations: list[str] = []
    data: dict = {}
    agents_used: list[str] = []


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "orchestration"}


@app.post("/api/v1/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """Process a natural language query through the agent graph."""
    # TODO: Initialize LangGraph, run agents, return results
    return QueryResponse(
        query=request.query,
        explanation="Agent orchestration not yet connected. This is a placeholder response.",
        recommendations=["Connect LangGraph agent pipeline", "Load ML models"],
        agents_used=[],
    )


@app.post("/api/v1/simulate")
async def run_simulation(scenario: dict):
    """Run a what-if simulation scenario."""
    # TODO: Pass scenario to simulation agent
    return {
        "scenario": scenario,
        "result": "Simulation not yet implemented",
        "impact": {},
    }


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time updates."""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # TODO: Stream real-time predictions and alerts
            await websocket.send_json({"type": "ack", "data": data})
    except WebSocketDisconnect:
        pass
