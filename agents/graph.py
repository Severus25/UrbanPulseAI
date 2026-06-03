"""UrbanPulse AI - Multi-Agent Orchestration with LangGraph"""

import os
import glob
import json
import logging
from typing import TypedDict, Annotated, Literal
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import SystemMessage, HumanMessage

# Try to import OpenAI, catch if not installed/configured
try:
    from langchain_openai import ChatOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

logger = logging.getLogger("urbanpulse.agents")


class UrbanPulseState(TypedDict):
    """Shared state across all agents in the graph."""
    messages: Annotated[list, add_messages]
    query: str
    location: dict | None
    time_range: dict | None
    traffic_data: dict | None
    weather_data: dict | None
    incident_data: dict | None
    risk_assessment: dict | None
    forecast: dict | None
    simulation_result: dict | None
    explanation: str | None
    recommendations: list[str]
    retrieved_docs: list[dict]  # RAG retrieved municipal guidelines
    routing_decision: str | None


# =============================================================================
# Helper: Local RAG (TF-IDF Term Match fallback / ChromaDB)
# =============================================================================
class LocalDocumentRetriever:
    """
    Retrieves municipal advisories.
    Uses simple keyword matching as a zero-dependency fallback for unit tests,
    but can be expanded to full vector-search using ChromaDB.
    """
    def __init__(self, search_dir: str = "data/municipal_advisories"):
        self.search_dir = search_dir

    def retrieve(self, query: str, top_k: int = 2) -> list[dict]:
        docs = []
        # Find all markdown files in data/municipal_advisories
        pattern = os.path.join(self.search_dir, "*.md")
        files = glob.glob(pattern)

        if not files:
            # Check absolute path fallback
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            fallback_dir = os.path.join(project_root, "data", "municipal_advisories")
            files = glob.glob(os.path.join(fallback_dir, "*.md"))

        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    filename = os.path.basename(file_path)
                    docs.append({
                        "source": filename,
                        "content": content
                    })
            except Exception as e:
                logger.error(f"Error reading file {file_path}: {e}")

        if not docs:
            return []

        # Pure Python basic search fallback
        query_words = set(query.lower().split())
        scored_docs = []
        for doc in docs:
            content_lower = doc["content"].lower()
            # Simple TF score: count overlaps
            score = sum(content_lower.count(word) for word in query_words)
            scored_docs.append((score, doc))

        # Sort by score descending and return top_k
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scored_docs[:top_k] if score > 0]


# =============================================================================
# Pydantic Schemas for Structured Tool Output
# =============================================================================
class QueryIntent(BaseModel):
    """Classifies the primary intent of the user's city query."""
    intent: Literal["traffic", "route", "policy", "simulate", "explain"] = Field(
        description="The target routing agent: traffic, route (mobility planning), policy (RAG lookup), simulate (what-if scenarios), or generic explain."
    )
    extracted_locations: list[str] = Field(
        default=[], description="Any street names, corridors, or landmarks mentioned in the query."
    )


# =============================================================================
# LangGraph Nodes
# =============================================================================

async def route_query(state: UrbanPulseState) -> UrbanPulseState:
    """Classify user query intent using LLM or rule-based fallback."""
    query = state.get("query", "")
    api_key = os.getenv("OPENAI_API_KEY")

    intent = None
    extracted_locations = []

    if OPENAI_AVAILABLE and api_key and not api_key.startswith("sk-your"):
        try:
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, api_key=api_key)
            structured_llm = llm.with_structured_output(QueryIntent)
            result = structured_llm.invoke(
                [
                    SystemMessage(content="You are the traffic routing controller for UrbanPulse AI. Categorize the user's intent."),
                    HumanMessage(content=query)
                ]
            )
            intent = result.intent
            extracted_locations = result.extracted_locations
        except Exception as e:
            logger.warning(f"LLM routing failed: {e}. Falling back to rule-based parser.")

    # Rule-based fallback
    if not intent:
        query_lower = query.lower()
        if any(w in query_lower for w in ["what if", "simulate", "scenario", "close", "lane reduction"]):
            intent = "simulate"
        elif any(w in query_lower for w in ["policy", "advisory", "notice", "regulation", "law", "rule"]):
            intent = "policy"
        elif any(w in query_lower for w in ["route", "path", "navigate", "fastest", "detour"]):
            intent = "route"
        elif any(w in query_lower for w in ["congestion", "traffic", "delay", "slow", "incident", "jam"]):
            intent = "traffic"
        else:
            intent = "explain"

        # Simple regex street name extractor
        for word in query.split():
            if word[0].isupper() and len(word) > 2 and word.lower() not in ["the", "what", "how", "where", "show"]:
                extracted_locations.append(word)

    state["routing_decision"] = intent
    state["location"] = {"extracted": extracted_locations}
    return state


def determine_next_agent(state: UrbanPulseState) -> str:
    """Determine the next edge based on the routing decision."""
    decision = state.get("routing_decision", "explain")
    if decision in ["traffic", "route", "policy", "simulate"]:
        return decision
    return "explain"


async def traffic_reasoner_agent(state: UrbanPulseState) -> UrbanPulseState:
    """Analyze traffic data and diagnose congestion causes."""
    query = state.get("query", "").lower()
    locations = state.get("location", {}).get("extracted", [])
    location_str = ", ".join(locations) if locations else "City Arterials"

    # Simulate fetching traffic stats from database
    traffic_data = {
        "corridor": location_str,
        "current_speed_kmh": 22.4,
        "free_flow_speed_kmh": 50.0,
        "congestion_index": 0.55,  # 0 to 1
        "peak_delay_seconds": 320
    }
    
    # Query incidents
    incident_data = {
        "active_incidents": [
            {
                "type": "Roadwork",
                "segment": "Broadway Corridor (Segment 105)",
                "description": "Right lane closed for utilities repair.",
                "severity": "moderate"
            }
        ]
    }

    # Inject data into state
    state["traffic_data"] = traffic_data
    state["incident_data"] = incident_data
    
    explanation = f"Traffic analysis for {location_str}: Current speeds are operating at {traffic_data['current_speed_kmh']} km/h (free flow: {traffic_data['free_flow_speed_kmh']} km/h). Congestion index is high at {traffic_data['congestion_index']:.2f}. "
    
    if incident_data["active_incidents"]:
        inc = incident_data["active_incidents"][0]
        explanation += f"This is aggravated by an active {inc['type']} incident on {inc['segment']}: {inc['description']}."
    
    state["explanation"] = explanation
    return state


async def mobility_planner_agent(state: UrbanPulseState) -> UrbanPulseState:
    """Provide intelligent route recommendation and detours based on hazards."""
    # Read weather or query to determine risk
    weather = state.get("weather_data") or {"precipitation_mm": 18.0} # default mock rain
    state["weather_data"] = weather

    recommendations = []
    
    # Check flooding risk
    if weather.get("precipitation_mm", 0) > 15.0:
        recommendations.append(
            "ALERT: River Valley Road (Segment 42) is closed due to flash flooding hazard. Avoid low-lying underpasses."
        )
        recommendations.append(
            "RECOMMENDATION: Reroute traffic via the Elevated Bypass (Segment 114). Est. travel time +4 mins, but 0% risk."
        )
    else:
        recommendations.append(
            "RECOMMENDATION: Use primary route via Broadway Corridor. Traffic speeds are normal."
        )

    state["recommendations"] = recommendations
    return state


async def policy_retrieval_agent(state: UrbanPulseState) -> UrbanPulseState:
    """Retrieve matching municipal advisory rules using search engine."""
    query = state.get("query", "")
    retriever = LocalDocumentRetriever()
    matched_docs = retriever.retrieve(query, top_k=2)
    
    state["retrieved_docs"] = matched_docs
    return state


async def simulation_agent(state: UrbanPulseState) -> UrbanPulseState:
    """Simulate infrastructure closures or changes to downstream flow."""
    query = state.get("query", "").lower()
    
    # Parse mock intervention parameters
    closed_segment = "Arena Way (Segment 102)"
    impacted_segments = ["Broadway Corridor (Segment 105)", "North Ring Road (Segment 88)"]
    
    sim_result = {
        "intervention": f"Complete closure of {closed_segment}",
        "downstream_impact": [
            {"segment": impacted_segments[0], "speed_change_pct": -35.0, "status": "severe_congestion"},
            {"segment": impacted_segments[1], "speed_change_pct": 12.0, "status": "increased_volume"}
        ],
        "system_delay_increase_seconds": 450
    }
    
    state["simulation_result"] = sim_result
    state["explanation"] = (
        f"SIMULATION RUN: Closing {closed_segment} will result in severe downstream traffic spillover "
        f"along the {impacted_segments[0]} corridor, reducing speeds by 35%."
    )
    return state


async def narrative_agent(state: UrbanPulseState) -> UrbanPulseState:
    """Generate final human-readable narrative combining data, models, and policy."""
    api_key = os.getenv("OPENAI_API_KEY")
    
    explanation_body = state.get("explanation") or "Analysis completed."
    recommendations = state.get("recommendations", [])
    retrieved_docs = state.get("retrieved_docs", [])
    sim_result = state.get("simulation_result")
    
    # Setup context block
    context = {
        "query": state.get("query"),
        "traffic": state.get("traffic_data"),
        "weather": state.get("weather_data"),
        "incidents": state.get("incident_data"),
        "simulation": sim_result,
        "recommendations": recommendations,
        "policies": [d["source"] for d in retrieved_docs]
    }

    if OPENAI_AVAILABLE and api_key and not api_key.startswith("sk-your"):
        try:
            # Call OpenAI to synthesize a beautiful narrative
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3, api_key=api_key)
            prompt = (
                "You are UrbanPulse AI, a smart digital twin city coordinator. Write a clear, "
                "professional, and action-oriented explanation responding to the user's city query. "
                "Synthesize the ML models, weather, active incidents, and retrieved municipal advisories.\n\n"
                f"Context data:\n{json.dumps(context, indent=2)}\n\n"
                f"Preliminary explanation: {explanation_body}\n\n"
                "Provide a beautifully formatted markdown report with sections: Cause Analysis, "
                "Policy Compliance, and Operator Recommendations."
            )
            response = llm.invoke([HumanMessage(content=prompt)])
            state["explanation"] = response.content
            return state
        except Exception as e:
            logger.warning(f"Narrative LLM generation failed: {e}. Using template formatter.")

    # Static rich formatting fallback
    lines = [
        f"### 🏙️ UrbanPulse AI Operator Report",
        f"**Query:** *\"{state.get('query')}\"*",
        f"\n#### 🔍 Cause Analysis",
        explanation_body
    ]

    if retrieved_docs:
        lines.append("\n#### 📜 Policy & Municipal Compliance")
        for doc in retrieved_docs:
            lines.append(f"- **From {doc['source']}:**")
            # Grab first 2 lines of markdown policy
            lines.append("  > " + "\n  > ".join(doc["content"].split("\n")[:4]))
            
    if recommendations:
        lines.append("\n#### 🛠️ Operator Action Plan")
        for rec in recommendations:
            lines.append(f"- {rec}")
            
    if sim_result:
        lines.append("\n#### 📊 What-If Simulation Results")
        lines.append(f"- **Intervention:** {sim_result['intervention']}")
        lines.append(f"- **System Delay Increase:** +{sim_result['system_delay_increase_seconds']} seconds")
        for imp in sim_result["downstream_impact"]:
            lines.append(f"  - Segment *{imp['segment']}*: speed changed by `{imp['speed_change_pct']}%` ({imp['status']})")

    state["explanation"] = "\n".join(lines)
    return state


# =============================================================================
# Graph Definition
# =============================================================================
def create_urbanpulse_graph():
    """Build the LangGraph agent orchestration graph."""
    graph = StateGraph(UrbanPulseState)

    # Add agent nodes
    graph.add_node("router", route_query)
    graph.add_node("traffic_reasoner", traffic_reasoner_agent)
    graph.add_node("mobility_planner", mobility_planner_agent)
    graph.add_node("policy_retrieval", policy_retrieval_agent)
    graph.add_node("simulation", simulation_agent)
    graph.add_node("narrative", narrative_agent)

    # Entry point
    graph.set_entry_point("router")

    # Conditional routing based on query type
    graph.add_conditional_edges(
        "router",
        determine_next_agent,
        {
            "traffic": "traffic_reasoner",
            "route": "mobility_planner",
            "policy": "policy_retrieval",
            "simulate": "simulation",
            "explain": "narrative",
        },
    )

    # All agents flow to narrative for final explanation
    graph.add_edge("traffic_reasoner", "narrative")
    graph.add_edge("mobility_planner", "narrative")
    graph.add_edge("policy_retrieval", "narrative")
    graph.add_edge("simulation", "narrative")
    graph.add_edge("narrative", END)

    return graph.compile()
