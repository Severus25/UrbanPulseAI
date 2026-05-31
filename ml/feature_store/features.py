"""Feature engineering pipeline for UrbanPulse ML models."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class TrafficFeatures:
    """Engineered features for traffic prediction models."""
    segment_id: str
    timestamp: datetime
    
    # Temporal features
    hour_of_day: int
    day_of_week: int
    is_weekend: bool
    is_holiday: bool
    minutes_since_midnight: int
    
    # Road characteristics
    segment_length_m: float
    num_lanes: int
    speed_limit_kmh: float
    road_type: str
    
    # Historical patterns
    historical_avg_speed: float
    historical_std_speed: float
    
    # Lag features
    lag_5min_speed: float
    lag_15min_speed: float
    lag_1h_speed: float
    lag_24h_speed: float
    
    # Weather features
    temperature_c: float
    precipitation_mm: float
    visibility_km: float
    wind_speed_kmh: float
    
    # Spatial neighborhood
    upstream_avg_speed: float
    downstream_avg_speed: float
    parallel_route_speed: float
    
    # Events
    nearby_events_count: int
    nearest_event_distance_km: float


class FeatureEngineer:
    """Transforms raw data into ML-ready features."""

    def extract_temporal_features(self, timestamp: datetime) -> dict:
        return {
            "hour_of_day": timestamp.hour,
            "day_of_week": timestamp.weekday(),
            "is_weekend": timestamp.weekday() >= 5,
            "is_holiday": False,  # TODO: integrate holiday calendar
            "minutes_since_midnight": timestamp.hour * 60 + timestamp.minute,
        }

    def extract_lag_features(self, speed_history: list[float], intervals: list[int]) -> dict:
        """Extract lag features from speed history at given intervals (in minutes)."""
        features = {}
        for interval in intervals:
            idx = interval  # assuming 1-minute resolution
            if idx < len(speed_history):
                features[f"lag_{interval}min_speed"] = speed_history[-(idx + 1)]
            else:
                features[f"lag_{interval}min_speed"] = 0.0
        return features

    def compute_spatial_features(self, segment_id: str, graph: dict) -> dict:
        """Compute features from neighboring road segments."""
        # TODO: Query road graph for upstream/downstream/parallel segments
        return {
            "upstream_avg_speed": 0.0,
            "downstream_avg_speed": 0.0,
            "parallel_route_speed": 0.0,
        }
