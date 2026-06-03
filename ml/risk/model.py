"""Risk Scoring Model - Combines weather, events, history for disruption risk."""

import numpy as np
from dataclasses import dataclass
from datetime import datetime


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
    - Historical incident frequency and severity
    - Current/forecast weather severity (precipitation, visibility)
    - Nearby event proximity and size
    - Current congestion level (speed ratio)
    """

    def __init__(self, weights: dict[str, float] | None = None):
        self.weights = weights or {
            "accident_history": 0.25,
            "weather_severity": 0.25,
            "event_proximity": 0.15,
            "congestion_level": 0.20,
            "road_condition": 0.15,
        }
        # Normalize weights to sum to 1.0
        total_weight = sum(self.weights.values())
        if total_weight > 0:
            self.weights = {k: v / total_weight for k, v in self.weights.items()}

    def compute_risk(
        self,
        segment_id: str,
        weather: dict | None = None,
        events: list[dict] | None = None,
        incident_history: list[dict] | None = None,
        current_traffic: dict | None = None,
    ) -> RiskScore:
        """
        Compute composite disruption risk for a road segment with robust default handlings.
        """
        # Ensure parameters are not None to avoid TypeErrors
        weather_dict = weather or {}
        event_list = events or []
        incident_list = incident_history or []
        traffic_dict = current_traffic or {}

        # Calculate sub-risks
        accident_risk = self._accident_risk(incident_list)
        flooding_risk = self._flooding_risk(weather_dict)
        congestion_risk = self._congestion_risk(traffic_dict)
        event_risk = self._event_risk(event_list)
        
        # Heuristic road condition score based on weather and age/type if present
        road_condition = self._road_condition_risk(weather_dict, traffic_dict)

        # Composite calculation
        overall = (
            self.weights.get("accident_history", 0.25) * accident_risk
            + self.weights.get("weather_severity", 0.25) * flooding_risk
            + self.weights.get("congestion_level", 0.20) * congestion_risk
            + self.weights.get("event_proximity", 0.15) * event_risk
            + self.weights.get("road_condition", 0.15) * road_condition
        )
        overall = float(np.clip(overall, 0.0, 1.0))

        # Identify contributing factors
        factors = []
        if flooding_risk >= 0.6:
            precip = weather_dict.get("precipitation_mm", 0)
            factors.append(f"Heavy precipitation detected ({precip}mm/h)")
        if accident_risk >= 0.6:
            factors.append(f"High historical accident frequency ({len(incident_list)} incidents)")
        if event_risk >= 0.5:
            factors.append("Active special event nearby creating local congestion")
        if congestion_risk >= 0.7:
            factors.append("Critical vehicle slowdown (gridlock conditions)")
        if road_condition >= 0.6:
            factors.append("Reduced road grip and wet driving surface conditions")

        # Generate recommended actions
        actions = self._recommend_actions(overall, factors, flooding_risk, accident_risk)

        return RiskScore(
            segment_id=segment_id,
            overall_risk=round(overall, 2),
            accident_risk=round(accident_risk, 2),
            flooding_risk=round(flooding_risk, 2),
            congestion_risk=round(congestion_risk, 2),
            event_disruption_risk=round(event_risk, 2),
            contributing_factors=factors,
            recommended_actions=actions,
        )

    def _accident_risk(self, history: list[dict]) -> float:
        """Assess historical crash patterns."""
        if not history:
            return 0.1
        
        # Calculate risk based on frequency and severity
        frequency_score = min(len(history) / 10.0, 1.0)
        
        severity_weights = {"major": 1.0, "moderate": 0.6, "minor": 0.3}
        severities = [severity_weights.get(inc.get("severity", "minor").lower(), 0.3) for inc in history]
        severity_score = float(np.mean(severities)) if severities else 0.3
        
        # Weighted combination of frequency and average severity
        risk = 0.5 * frequency_score + 0.5 * severity_score
        return float(np.clip(risk, 0.0, 1.0))

    def _flooding_risk(self, weather: dict) -> float:
        """Estimate road flooding risk based on precipitation."""
        precip = float(weather.get("precipitation_mm", 0.0) or 0.0)
        # Precipitation-based heuristics
        if precip >= 30.0:
            return 0.95
        elif precip >= 15.0:
            return 0.75
        elif precip >= 5.0:
            return 0.45
        elif precip >= 1.0:
            return 0.20
        return 0.05

    def _congestion_risk(self, traffic: dict) -> float:
        """Compute risk based on speed relative to free flow speed."""
        current = float(traffic.get("current_speed", 50.0) or 50.0)
        free_flow = float(traffic.get("free_flow_speed", 50.0) or 50.0)
        
        if free_flow <= 0:
            free_flow = 50.0
            
        ratio = current / free_flow
        # Lower ratio means higher risk of gridlock / delay
        risk = 1.0 - ratio
        return float(np.clip(risk, 0.0, 1.0))

    def _event_risk(self, events: list[dict]) -> float:
        """Estimate event impact based on size and proximity."""
        if not events:
            return 0.0
        
        risks = []
        for e in events:
            attendance = float(e.get("expected_attendance", 0) or 0)
            distance = float(e.get("distance_km", 1.0) or 1.0)
            
            # Larger events and closer events present higher risk
            size_score = min(attendance / 60000.0, 1.0)
            proximity_score = max(0.0, 1.0 - (distance / 3.0)) # 0 risk beyond 3km
            
            risks.append(size_score * proximity_score)
            
        return float(np.max(risks)) if risks else 0.0

    def _road_condition_risk(self, weather: dict, traffic: dict) -> float:
        """Estimate surface slickness/condition degradation."""
        temp = float(weather.get("temperature_c", 20.0) or 20.0)
        precip = float(weather.get("precipitation_mm", 0.0) or 0.0)
        
        condition = 0.1
        if precip > 0:
            if temp <= 0:
                condition = 0.95  # Icy road risk
            else:
                condition = 0.55  # Wet hydroplane risk
        elif temp <= -2:
            condition = 0.3  # Frost hazard
            
        return condition

    def _recommend_actions(self, risk: float, factors: list[str], flooding_risk: float, accident_risk: float) -> list[str]:
        """Generate tactical operator recommendations based on threat levels."""
        actions = []
        if risk >= 0.75:
            actions.append("Critical Alert: Broadcast detour advice on electronic dynamic signs")
            actions.append("Alert local transit operators of severe delays")
        elif risk >= 0.45:
            actions.append("Advise drivers to maintain safe stopping distances")
            actions.append("Dispatch transit patrol to monitor flow")

        if flooding_risk >= 0.7:
            actions.append("Activate low-lying zone drainage pump systems")
            actions.append("Prepare emergency barriers for lane closures")
        
        if accident_risk >= 0.7:
            actions.append("Deploy traffic safety officer / service patrol to high-risk sector")

        if not actions:
            actions.append("No immediate intervention required. Maintain baseline monitoring.")
            
        return actions
