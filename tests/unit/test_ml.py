"""Unit tests for spatiotemporal machine learning models."""

import os
import tempfile
import numpy as np
import pytest
import torch
from ml.congestion.model import CongestionForecaster, CongestionPrediction, TrafficGCN
from ml.risk.model import DisruptionRiskModel, RiskScore


def test_xgboost_forecaster_train_predict():
    """Verify that the XGBoost congestion forecaster trains and predicts correctly."""
    forecaster = CongestionForecaster()
    
    # 10 samples, 17 features each
    n_samples = 10
    n_features = len(forecaster.feature_columns)
    
    # Generate mock features and targets
    np.random.seed(42)
    features = np.random.rand(n_samples, n_features) * 50.0
    # Set speed limit feature (index 6) to 50 km/h so ratio calculation works cleanly
    features[:, 6] = 50.0
    # Set historical std speed (index 8) to 5.0
    features[:, 8] = 5.0
    
    targets = np.random.rand(n_samples) * 50.0

    # Train model
    forecaster.train(features, targets)

    # Predict
    preds = forecaster.predict(features)
    assert len(preds) == n_samples
    for p in preds:
        assert isinstance(p, CongestionPrediction)
        assert isinstance(p.segment_id, str)
        assert isinstance(p.predicted_speed_kmh, float)
        assert p.congestion_level in ["free_flow", "moderate", "heavy", "gridlock"]
        assert 0.0 <= p.confidence <= 1.0
        assert isinstance(p.contributing_factors, list)


def test_shap_explainability():
    """Verify that the SHAP explanation logic functions without error."""
    forecaster = CongestionForecaster()
    n_samples = 5
    n_features = len(forecaster.feature_columns)
    
    np.random.seed(42)
    features = np.random.rand(n_samples, n_features) * 40.0
    targets = np.random.rand(n_samples) * 40.0
    
    # Train
    forecaster.train(features, targets)
    
    # Explain single sample
    explanation = forecaster.explain(features[0:1])
    assert "top_factors" in explanation
    assert "shap_values" in explanation
    assert len(explanation["top_factors"]) <= 3
    for k in forecaster.feature_columns:
        assert k in explanation["shap_values"]


def test_pytorch_gcn():
    """Verify that our pure PyTorch GCN model executes forward pass and trains successfully."""
    n_nodes = 5
    in_features = 17
    
    # Adjacency matrix representing a simple ring graph
    adj = np.array([
        [0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1],
        [1, 0, 0, 1, 0]
    ], dtype=np.float32)
    
    # Node features and targets
    x = np.random.rand(n_nodes, in_features).astype(np.float32)
    y = np.random.rand(n_nodes).astype(np.float32) * 60.0
    
    forecaster = CongestionForecaster()
    
    # Train GCN
    forecaster.train_gcn(x, adj, y, epochs=5)
    assert isinstance(forecaster.gcn_model, TrafficGCN)
    
    # Predict GCN
    preds = forecaster.predict_gcn(x, adj)
    assert preds.shape == (n_nodes,)


def test_forecaster_save_load():
    """Verify that models can be saved and reloaded from disk."""
    forecaster = CongestionForecaster()
    n_features = len(forecaster.feature_columns)
    
    x = np.random.rand(5, n_features)
    y = np.array([30.0, 40.0, 50.0, 60.0, 45.0])
    
    forecaster.train(x, y)
    
    # Train GCN so that we have weights to save
    adj = np.eye(5)
    forecaster.train_gcn(x, adj, y, epochs=2)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        model_path = os.path.join(tmpdir, "test_model")
        forecaster.save(model_path)
        
        # Load into new instance
        new_forecaster = CongestionForecaster()
        new_forecaster.load(model_path)
        
        assert new_forecaster.model is not None
        assert new_forecaster.gcn_model is not None
        
        # Make predictions to verify loaded model works
        preds = new_forecaster.predict(x)
        assert len(preds) == 5


def test_disruption_risk_model():
    """Verify that composite risk scores calculate correctly and reflect factors."""
    model = DisruptionRiskModel()
    
    # Test case 1: Baseline / Low-Risk Scenario
    low_risk_score = model.compute_risk(
        segment_id="seg_01",
        weather={"precipitation_mm": 0.0, "temperature_c": 20.0},
        events=[],
        incident_history=[],
        current_traffic={"current_speed": 50.0, "free_flow_speed": 50.0}
    )
    assert isinstance(low_risk_score, RiskScore)
    assert low_risk_score.overall_risk < 0.3
    assert len(low_risk_score.contributing_factors) == 0
    assert "No immediate intervention" in low_risk_score.recommended_actions[0]

    # Test case 2: High Precipitation / Flooding Risk Scenario
    flood_risk_score = model.compute_risk(
        segment_id="seg_01",
        weather={"precipitation_mm": 35.0, "temperature_c": 15.0},
        events=[],
        incident_history=[],
        current_traffic={"current_speed": 45.0, "free_flow_speed": 50.0}
    )
    assert flood_risk_score.flooding_risk >= 0.9
    assert any("precipitation" in f.lower() for f in flood_risk_score.contributing_factors)
    assert any("drainage" in a.lower() for a in flood_risk_score.recommended_actions)

    # Test case 3: Extreme Congestion Scenario
    congested_risk_score = model.compute_risk(
        segment_id="seg_01",
        weather={"precipitation_mm": 0.0},
        events=[],
        incident_history=[],
        current_traffic={"current_speed": 10.0, "free_flow_speed": 50.0}
    )
    assert congested_risk_score.congestion_risk >= 0.8
    assert any("slowdown" in f.lower() for f in congested_risk_score.contributing_factors)
