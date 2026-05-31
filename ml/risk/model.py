"""Risk Scoring Model - Combines weather, events, history for disruption risk."""

import numpy as np
from dataclasses import dataclass


@dataclass
class RiskScore:
    segment_id: str
    overall_risk: float  # 0-1
    accident_risk: float
    flooding_risk: float
    congestion_risk: float
    event_disruption_risk: float
    contributing_factors: list[str]
    recommended_actions: list[str]


class DisruptionRiskModel:
    """
    Computes a composite risk score for road segments by combining:
    - Historical incident frequency
    - Current/forecast weather conditions
    - Nearby events
    - Road characteristics
    - Time-of-day patterns
    """

    def __init__(self):
        self.weights = {
            "accident_history": 0.25,
            "weather_severity": 0.25,
            "event_proximity": 0.15,
            "congestion_level": 0.20,
            "road_condition": 0.15,
        }

    def compute_risk(
        self,
        segment_id: str,
        weather: dict,
        events: list[dict],
        incident_history: list[dict],
        current_traffic: dict,
    ) -> RiskScore:
        """Compute composite disruption risk for a road segment."""
        accident_risk = self._accident_risk(incident_history)
        flooding_risk = self._flooding_risk(weather)
        congestion_risk = self._congestion_risk(current_traffic)
        event_risk = self._event_risk(events)

        overall = (
            self.weights["accident_history"] * accident_risk
            + self.weights["weather_severity"] * flooding_risk
            + self.weights["congestion_level"] * congestion_risk
            + self.weights["event_proximity"] * event_risk
        )

        factors = []
        if flooding_risk > 0.6:
            factors.append("Heavy precipitation expected")
        if accident_risk > 0.6:
            factors.append("High historical accident rate")
        if event_risk > 0.5:
            factors.append("Nearby event causing traffic surge")

        return RiskScore(
            segment_id=segment_id,
            overall_risk=min(overall, 1.0),
            accident_risk=accident_risk,
            flooding_risk=flooding_risk,
            congestion_risk=congestion_risk,
            event_disruption_risk=event_risk,
            contributing_factors=factors,
            recommended_actions=self._recommend_actions(overall, factors),
        )

    def _accident_risk(self, history: list[dict]) -> float:
        if not history:
            return 0.1
        # Normalize by frequency
        return min(len(history) / 20.0, 1.0)

    def _flooding_risk(self, weather: dict) -> float:
        precip = weather.get("precipitation_mm", 0)
        if precip > 50:
            return 0.9
        elif precip > 25:
            return 0.6
        elif precip > 10:
            return 0.3
        return 0.05

    def _congestion_risk(self, traffic: dict) -> float:
        speed_ratio = traffic.get("current_speed", 60) / traffic.get("free_flow_speed", 60)
        return max(0, 1.0 - speed_ratio)

    def _event_risk(self, events: list[dict]) -> float:
        if not events:
            return 0.0
        # Simple heuristic based on event size
        max_attendance = max(e.get("expected_attendance", 0) for e in events)
        return min(max_attendance / 50000, 1.0)

    def _recommend_actions(self, risk: float, factors: list[str]) -> list[str]:
        actions = []
        if risk > 0.7:
            actions.append("Consider route alternatives")
            actions.append("Deploy traffic management resources")
        if "Heavy precipitation" in str(factors):
            actions.append("Activate flood monitoring for low-lying segments")
        return actions
