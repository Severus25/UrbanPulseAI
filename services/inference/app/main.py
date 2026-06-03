"""UrbanPulse AI - Inference Service"""

import os
import sys
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel

# Add project root to sys.path to enable imports of the ml folder
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from ml.congestion.model import CongestionForecaster
from ml.risk.model import DisruptionRiskModel

app = FastAPI(title="UrbanPulse AI - Inference Service", version="0.1.0")

# Initialize models
forecaster = CongestionForecaster()
risk_model = DisruptionRiskModel()


class PredictionRequest(BaseModel):
    model_name: str  # congestion, eta, risk, incident, vision
    segment_id: str | None = None
    lat: float | None = None
    lon: float | None = None
    features: dict = {}


class PredictionResponse(BaseModel):
    model_name: str
    prediction: dict
    confidence: float
    explanation: dict | None = None


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "inference"}


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Run model inference."""
    try:
        if request.model_name == "congestion":
            # Map request features to numerical array required by model
            feat_list = []
            for col in forecaster.feature_columns:
                # Get feature value (defaulting to 0.0)
                feat_list.append(float(request.features.get(col, 0.0)))
            features_arr = np.array([feat_list])

            segment_id = request.segment_id or "segment_unknown"
            pred_list = forecaster.predict(features_arr, segment_ids=[segment_id])
            pred = pred_list[0]

            explanation = forecaster.explain(features_arr)

            return PredictionResponse(
                model_name=request.model_name,
                prediction={
                    "predicted_speed_kmh": pred.predicted_speed_kmh,
                    "congestion_level": pred.congestion_level,
                    "contributing_factors": pred.contributing_factors,
                },
                confidence=pred.confidence,
                explanation=explanation,
            )

        elif request.model_name == "risk":
            segment_id = request.segment_id or "segment_unknown"
            weather = request.features.get("weather", {})
            events = request.features.get("events", [])
            incident_history = request.features.get("incident_history", [])
            current_traffic = request.features.get("current_traffic", {})

            risk_score = risk_model.compute_risk(
                segment_id=segment_id,
                weather=weather,
                events=events,
                incident_history=incident_history,
                current_traffic=current_traffic,
            )

            return PredictionResponse(
                model_name=request.model_name,
                prediction={
                    "overall_risk": risk_score.overall_risk,
                    "accident_risk": risk_score.accident_risk,
                    "flooding_risk": risk_score.flooding_risk,
                    "congestion_risk": risk_score.congestion_risk,
                    "event_disruption_risk": risk_score.event_disruption_risk,
                    "contributing_factors": risk_score.contributing_factors,
                    "recommended_actions": risk_score.recommended_actions,
                },
                confidence=round(1.0 - risk_score.overall_risk, 2),
                explanation={
                    "contributing_factors": risk_score.contributing_factors,
                    "recommended_actions": risk_score.recommended_actions,
                },
            )

        else:
            # Fallback stub response for other models
            return PredictionResponse(
                model_name=request.model_name,
                prediction={"value": 0, "label": "unknown", "status": "stub_not_implemented"},
                confidence=0.0,
                explanation=None,
            )

    except Exception as e:
        return PredictionResponse(
            model_name=request.model_name,
            prediction={"error": str(e)},
            confidence=0.0,
            explanation={"error_details": str(e)},
        )


@app.get("/models")
async def list_models():
    """List available models and their status."""
    return {
        "models": [
            {"name": "congestion_xgboost", "status": "loaded", "version": "0.1.0"},
            {"name": "congestion_gnn", "status": "loaded", "version": "0.1.0"},
            {"name": "risk_scorer", "status": "loaded", "version": "0.1.0"},
            {"name": "eta_regression", "status": "stub", "version": "0.1.0"},
            {"name": "incident_detector", "status": "stub", "version": "0.1.0"},
            {"name": "traffic_vision_yolo", "status": "stub", "version": "0.1.0"},
        ]
    }
