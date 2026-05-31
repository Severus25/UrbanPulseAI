"""UrbanPulse AI - Database models (SQLAlchemy + PostGIS)"""

from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, JSON
from sqlalchemy.orm import declarative_base
from geoalchemy2 import Geometry

Base = declarative_base()


class RoadSegment(Base):
    """Road network segments derived from OpenStreetMap."""
    __tablename__ = "road_segments"

    id = Column(String, primary_key=True)
    osm_way_id = Column(String, index=True)
    name = Column(String)
    road_type = Column(String)  # motorway, primary, secondary, etc.
    speed_limit_kmh = Column(Float)
    num_lanes = Column(Integer)
    length_m = Column(Float)
    geometry = Column(Geometry("LINESTRING", srid=4326))
    created_at = Column(DateTime, default=datetime.utcnow)


class TrafficObservation(Base):
    """Real-time traffic speed observations per segment."""
    __tablename__ = "traffic_observations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    segment_id = Column(String, index=True)
    timestamp = Column(DateTime, index=True)
    speed_kmh = Column(Float)
    free_flow_speed_kmh = Column(Float)
    congestion_ratio = Column(Float)  # current/freeflow
    confidence = Column(Float)
    source = Column(String)


class Incident(Base):
    """Traffic incidents and road events."""
    __tablename__ = "incidents"

    id = Column(String, primary_key=True)
    incident_type = Column(String)  # accident, construction, closure, event
    severity = Column(Integer)  # 1-5
    description = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    location = Column(Geometry("POINT", srid=4326))
    affected_segments = Column(JSON)  # list of segment IDs
    source = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class WeatherRecord(Base):
    """Weather observations and forecasts."""
    __tablename__ = "weather_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, index=True)
    forecast_for = Column(DateTime)  # null if observation
    location = Column(Geometry("POINT", srid=4326))
    temperature_c = Column(Float)
    humidity_pct = Column(Float)
    precipitation_mm = Column(Float)
    visibility_km = Column(Float)
    wind_speed_kmh = Column(Float)
    condition = Column(String)
    is_forecast = Column(Boolean, default=False)


class RiskScore(Base):
    """Computed risk scores per segment."""
    __tablename__ = "risk_scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    segment_id = Column(String, index=True)
    timestamp = Column(DateTime, index=True)
    overall_risk = Column(Float)
    accident_risk = Column(Float)
    flooding_risk = Column(Float)
    congestion_risk = Column(Float)
    event_risk = Column(Float)
    contributing_factors = Column(JSON)


class CameraFeed(Base):
    """Traffic camera metadata."""
    __tablename__ = "camera_feeds"

    id = Column(String, primary_key=True)
    name = Column(String)
    location = Column(Geometry("POINT", srid=4326))
    feed_url = Column(String)
    is_active = Column(Boolean, default=True)
    last_frame_at = Column(DateTime, nullable=True)
