# UrbanPulse AI - API Specification

## Overview

The UrbanPulse AI platform exposes a RESTful API through the **Data Gateway** service. All endpoints follow consistent conventions for authentication, error handling, and response formatting.

**Base URL**: `http://localhost:8100` (development)

**Interactive Docs**:
- Swagger UI: `http://localhost:8100/docs`
- ReDoc: `http://localhost:8100/redoc`

---

## Authentication

All API requests (except `/health`) require a valid JWT bearer token:

```
Authorization: Bearer <token>
```

Tokens are issued via the `/auth/token` endpoint and expire after 24 hours.

---

## Common Response Format

### Success Response

```json
{
  "status": "success",
  "data": { ... },
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "req_abc123",
    "processing_time_ms": 45
  }
}
```

### Error Response

```json
{
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid parameter: lat must be between -90 and 90",
    "details": [...]
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "req_abc123"
  }
}
```

### HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Resource created |
| 400 | Bad request / validation error |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Unprocessable entity |
| 429 | Rate limit exceeded |
| 500 | Internal server error |
| 503 | Service unavailable |

---

## Endpoints

### Health & Status

#### `GET /health`

Returns service health status. No authentication required.

**Response:**
```json
{
  "status": "healthy",
  "service": "data-gateway",
  "version": "0.1.0",
  "dependencies": {
    "postgres": "connected",
    "redis": "connected",
    "kafka": "connected"
  }
}
```

---

### Traffic

#### `GET /api/v1/traffic/flow`

Returns real-time traffic flow data for a geographic area.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `bbox` | string | Yes | Bounding box (min_lon,min_lat,max_lon,max_lat) |
| `zoom` | integer | No | Map zoom level for aggregation (default: 12) |

**Response:**
```json
{
  "status": "success",
  "data": {
    "segments": [
      {
        "id": "seg_001",
        "geometry": { "type": "LineString", "coordinates": [...] },
        "properties": {
          "speed_kmh": 45.2,
          "free_flow_speed_kmh": 60.0,
          "congestion_level": 0.25,
          "confidence": 0.92,
          "updated_at": "2024-01-15T10:29:00Z"
        }
      }
    ]
  }
}
```

#### `GET /api/v1/traffic/congestion`

Returns congestion predictions for the next 1-4 hours.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `bbox` | string | Yes | Bounding box |
| `horizon_hours` | integer | No | Prediction horizon (1-4, default: 2) |
| `include_explanation` | boolean | No | Include AI explanation (default: false) |

**Response:**
```json
{
  "status": "success",
  "data": {
    "predictions": [
      {
        "segment_id": "seg_001",
        "predicted_congestion": 0.72,
        "confidence_interval": [0.65, 0.79],
        "predicted_speed_kmh": 22.5,
        "horizon": "2024-01-15T12:30:00Z",
        "contributing_factors": [
          { "factor": "rush_hour", "weight": 0.4 },
          { "factor": "rain_forecast", "weight": 0.3 },
          { "factor": "event_nearby", "weight": 0.2 }
        ]
      }
    ],
    "explanation": "High congestion expected due to evening rush hour combined with incoming rain..."
  }
}
```

---

### Transit

#### `GET /api/v1/transit/delays`

Returns current and predicted transit delays.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `route_id` | string | No | Filter by specific route |
| `stop_id` | string | No | Filter by specific stop |
| `bbox` | string | No | Geographic filter |

**Response:**
```json
{
  "status": "success",
  "data": {
    "delays": [
      {
        "route_id": "bus_42",
        "route_name": "Downtown Express",
        "stop_id": "stop_1234",
        "scheduled_time": "2024-01-15T10:30:00Z",
        "predicted_time": "2024-01-15T10:37:00Z",
        "delay_seconds": 420,
        "cause": "traffic_congestion",
        "confidence": 0.85
      }
    ]
  }
}
```

---

### Weather

#### `GET /api/v1/weather/current`

Returns current weather conditions with traffic impact assessment.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `lat` | float | Yes | Latitude |
| `lon` | float | Yes | Longitude |

**Response:**
```json
{
  "status": "success",
  "data": {
    "conditions": {
      "temperature_c": 8.5,
      "humidity_pct": 78,
      "precipitation_mm": 2.1,
      "wind_speed_kmh": 15.3,
      "visibility_km": 5.2,
      "condition": "rain"
    },
    "traffic_impact": {
      "risk_multiplier": 1.35,
      "speed_reduction_pct": 15,
      "incident_risk_increase_pct": 22
    },
    "forecast_hours": [
      {
        "hour": 1,
        "condition": "rain",
        "precipitation_mm": 3.2
      }
    ]
  }
}
```

---

### Incidents

#### `GET /api/v1/incidents`

Returns active and predicted incidents.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `bbox` | string | Yes | Bounding box |
| `status` | string | No | Filter: active, resolved, predicted |
| `severity` | string | No | Filter: low, medium, high, critical |

**Response:**
```json
{
  "status": "success",
  "data": {
    "incidents": [
      {
        "id": "inc_567",
        "type": "accident",
        "severity": "high",
        "status": "active",
        "location": {
          "lat": 40.7128,
          "lon": -74.0060,
          "road_name": "Broadway",
          "segment_id": "seg_089"
        },
        "detected_at": "2024-01-15T10:15:00Z",
        "estimated_clearance": "2024-01-15T11:30:00Z",
        "affected_routes": ["bus_42", "bus_15"],
        "description": "Multi-vehicle collision blocking 2 lanes"
      }
    ]
  }
}
```

---

### Cameras

#### `GET /api/v1/cameras/feed`

Returns traffic camera feeds with AI analysis.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `bbox` | string | No | Geographic filter |
| `camera_id` | string | No | Specific camera |
| `include_analysis` | boolean | No | Include CV analysis (default: true) |

**Response:**
```json
{
  "status": "success",
  "data": {
    "cameras": [
      {
        "id": "cam_101",
        "name": "5th Ave & 42nd St",
        "location": { "lat": 40.7549, "lon": -73.9840 },
        "frame_url": "https://storage/frames/cam_101_latest.jpg",
        "analysis": {
          "vehicle_count": 23,
          "pedestrian_count": 45,
          "congestion_visual": "moderate",
          "incident_detected": false,
          "analyzed_at": "2024-01-15T10:29:55Z"
        }
      }
    ]
  }
}
```

---

## WebSocket API

### `WS /ws/live`

Real-time updates stream via WebSocket connection.

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8100/ws/live?token=<jwt>');
```

**Subscribe to channels:**
```json
{
  "action": "subscribe",
  "channels": ["traffic.flow", "incidents", "transit.delays"]
}
```

**Message format:**
```json
{
  "channel": "traffic.flow",
  "event": "update",
  "data": {
    "segment_id": "seg_001",
    "speed_kmh": 35.2,
    "congestion_level": 0.45
  },
  "timestamp": "2024-01-15T10:30:01Z"
}
```

**Available channels:**

| Channel | Description | Update Frequency |
|---------|-------------|-----------------|
| `traffic.flow` | Speed/congestion updates | Every 30s |
| `traffic.predictions` | New predictions available | Every 5min |
| `incidents` | Incident create/update/resolve | On event |
| `transit.delays` | Delay updates | Every 60s |
| `weather.alerts` | Weather warnings | On event |

---

## Rate Limiting

| Tier | Requests/min | WebSocket connections |
|------|-------------|---------------------|
| Free | 60 | 1 |
| Standard | 300 | 5 |
| Enterprise | Unlimited | Unlimited |

Rate limit headers are included in every response:
```
X-RateLimit-Limit: 300
X-RateLimit-Remaining: 287
X-RateLimit-Reset: 1705312260
```

---

## Pagination

List endpoints support cursor-based pagination:

```
GET /api/v1/incidents?limit=20&cursor=eyJpZCI6MTAwfQ==
```

Response includes pagination metadata:
```json
{
  "meta": {
    "pagination": {
      "has_next": true,
      "next_cursor": "eyJpZCI6MTIwfQ==",
      "total_count": 256
    }
  }
}
```

---

## Versioning

The API is versioned via URL path (`/api/v1/`). Breaking changes will increment the version number. Non-breaking additions (new fields, new endpoints) are added without version change.
