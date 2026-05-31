# 🏙️ UrbanPulse AI

[![CI/CD Pipeline](https://github.com/YOUR_USERNAME/UrbanPulse_AI/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/UrbanPulse_AI/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![Node.js 20+](https://img.shields.io/badge/node.js-20%2B-green.svg)](https://nodejs.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

**A Multimodal City Digital Twin for Traffic, Transit, Weather, and Risk-Aware Mobility**

> A real-time AI platform that predicts congestion, transit delays, accident risk, flooding/heat impact, and route disruptions — then explains the "why," simulates interventions, and recommends better routing or city operations decisions.

---

## Table of Contents

- [What It Does](#-what-it-does)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Prerequisites](#-prerequisites)
- [Quick Start](#-quick-start)
- [Development](#-development)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [API Documentation](#-api-documentation)
- [Key Features](#-key-features)
- [Configuration](#-configuration)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🧠 What It Does

UrbanPulse AI acts as a **city intelligence platform** that ingests multiple signal types:

- 🚗 Road traffic data (GPS speed feeds)
- 🚌 Public transit feeds (GTFS + real-time delays)
- 🌦️ Weather forecasts & air quality
- 🚧 Road incidents & closures
- 📅 Event schedules
- 📷 Traffic camera snapshots
- 🗺️ Road network topology (OSM)
- 📄 Municipal advisories / PDFs

And answers questions like:
- "Which areas will face abnormal congestion in the next 2 hours?"
- "How will heavy rain affect travel time and accident risk?"
- "What is the likely cause of unusual delays in this corridor?"
- "If the city closes one lane here, what downstream effect might happen?"

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                        APPLICATION LAYER                              │
│  Next.js + React + Mapbox/Deck.gl │ FastAPI Backend │ WebSocket      │
├──────────────────────────────────────────────────────────────────────┤
│                        AI REASONING LAYER                             │
│  LangGraph Multi-Agent │ Traffic Reasoner │ Mobility Planner │       │
│  Policy Retrieval │ Simulation Agent │ Narrative Agent                │
├──────────────────────────────────────────────────────────────────────┤
│                        ML LAYER                                       │
│  Congestion Forecasting │ Incident Detection │ ETA Prediction │      │
│  Risk Scoring │ Vision (Vehicle Density / Incident Detection)         │
├──────────────────────────────────────────────────────────────────────┤
│                        PROCESSING + FEATURE ENGINEERING               │
│  Map Matching │ Temporal Features │ Geospatial Joins │ Embeddings    │
├──────────────────────────────────────────────────────────────────────┤
│                        DATA INGESTION LAYER                           │
│  Kafka │ Airflow │ FastAPI Gateway │ PostGIS │ Object Storage        │
└──────────────────────────────────────────────────────────────────────┘
```

> For detailed architecture documentation, see [docs/architecture.md](docs/architecture.md).

---

## 📂 Project Structure

```
UrbanPulse_AI/
├── services/                  # Microservices (FastAPI)
│   ├── data-gateway/          #   Data ingestion & serving API
│   ├── inference/             #   ML model serving & predictions
│   ├── orchestration/         #   Agent orchestration (LangGraph)
│   ├── retrieval/             #   RAG / vector retrieval service
│   └── simulation/            #   What-if simulation engine
├── ml/                        # Machine Learning models
│   ├── congestion/            #   Traffic congestion forecasting
│   ├── incident/              #   Anomaly & incident detection
│   ├── eta/                   #   ETA / travel time prediction
│   ├── risk/                  #   Disruption risk scoring
│   ├── vision/                #   CV models (YOLOv8)
│   └── feature_store/         #   Feature engineering pipelines
├── agents/                    # LangGraph AI agents
│   ├── graph.py               #   Agent orchestration graph
│   ├── traffic_reasoner/      #   Explains congestion causes
│   ├── mobility_planner/      #   Route recommendations
│   ├── policy_retrieval/      #   Advisory document retrieval
│   ├── simulation_agent/      #   Counterfactual scenarios
│   └── narrative_agent/       #   Summary generation
├── pipelines/                 # Data pipelines
│   ├── airflow/               #   Airflow DAGs
│   ├── kafka/                 #   Kafka configs & consumers
│   └── etl/                   #   ETL scripts
├── frontend/                  # Next.js + React + Mapbox
├── infrastructure/            # Infrastructure as Code
│   ├── docker/                #   Dockerfiles
│   ├── k8s/                   #   Kubernetes manifests
│   ├── terraform/             #   Terraform configs
│   └── monitoring/            #   Prometheus, Grafana
├── tests/                     # Test suites
│   ├── unit/                  #   Unit tests
│   ├── integration/           #   Integration tests
│   └── e2e/                   #   End-to-end tests
├── docs/                      # Documentation
│   ├── architecture.md        #   System architecture
│   ├── api-spec.md            #   API specification
│   └── deployment.md          #   Deployment guide
├── .github/workflows/         # CI/CD pipelines
├── docker-compose.yml         # Local development stack
├── pyproject.toml             # Python project config
├── .env.example               # Environment variable template
├── CONTRIBUTING.md            # Contribution guidelines
├── CHANGELOG.md               # Version history
└── README.md                  # This file
```

---

## 🛠️ Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | Next.js 15, React 18, TypeScript, Mapbox GL JS, Deck.gl |
| **Backend** | FastAPI, Python 3.11+, WebSockets, Pydantic v2 |
| **ML** | PyTorch, scikit-learn, XGBoost, Temporal Fusion Transformer |
| **Vision** | YOLOv8 (Ultralytics), OpenCV, torchvision |
| **Agents** | LangGraph, LangChain, OpenAI GPT-4o |
| **Streaming** | Apache Kafka, Kafka Connect |
| **Orchestration** | Apache Airflow |
| **Databases** | PostgreSQL 16 + PostGIS, Redis 7, ChromaDB (vector store) |
| **Storage** | MinIO (S3-compatible), Parquet/Delta Lake |
| **Infrastructure** | Docker, Kubernetes, Terraform |
| **CI/CD** | GitHub Actions |
| **Observability** | OpenTelemetry, Prometheus, Grafana, structlog |

---

## 📋 Prerequisites

- **Python** >= 3.11
- **Node.js** >= 20
- **Docker** & **Docker Compose** (for full stack)
- **Git**

Optional (for ML training):
- NVIDIA GPU with CUDA 12+
- 16 GB+ RAM recommended

---

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/UrbanPulse_AI.git
cd UrbanPulse_AI

# Configure environment
cp .env.example .env
# Edit .env with your API keys (OpenAI, Mapbox, OpenWeatherMap)

# Start all services
docker-compose up -d

# Verify services
curl http://localhost:8100/health   # Data Gateway
open http://localhost:3000          # Frontend
```

### Option 2: Local Development (Without Docker)

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/UrbanPulse_AI.git
cd UrbanPulse_AI

# Configure environment
cp .env.example .env

# Backend setup
pip install fastapi uvicorn pydantic pydantic-settings websockets redis sqlalchemy asyncpg
cd services/data-gateway
uvicorn app.main:app --host 0.0.0.0 --port 8100 --reload

# Frontend setup (in a new terminal)
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:3000` and the API at `http://localhost:8100`.

---

## 🔧 Development

### Backend Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run linter
ruff check .

# Run type checker
mypy services/

# Format code
ruff format .
```

### Frontend Development

```bash
cd frontend

# Development server (hot reload)
npm run dev

# Type checking
npm run type-check

# Linting
npm run lint

# Build for production
npm run build
```

### Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install
```

---

## 🧪 Testing

```bash
# Run all Python tests
pytest

# Run with coverage
pytest --cov=services --cov=ml --cov=agents --cov-report=html

# Run specific test suites
pytest tests/unit/              # Unit tests only
pytest tests/integration/       # Integration tests (requires services)
pytest tests/e2e/               # End-to-end tests

# Frontend tests
cd frontend && npm test
```

---

## 🚢 Deployment

See [docs/deployment.md](docs/deployment.md) for detailed deployment instructions covering:

- Kubernetes deployment with Helm charts
- Terraform infrastructure provisioning
- CI/CD pipeline configuration
- Production environment setup
- Monitoring and alerting

---

## 📡 API Documentation

When the backend is running, interactive API docs are available at:

- **Swagger UI**: http://localhost:8100/docs
- **ReDoc**: http://localhost:8100/redoc

See [docs/api-spec.md](docs/api-spec.md) for the full API specification.

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Service health check |
| `GET` | `/api/v1/traffic/flow` | Real-time traffic flow data |
| `GET` | `/api/v1/traffic/congestion` | Congestion predictions |
| `GET` | `/api/v1/transit/delays` | Transit delay information |
| `GET` | `/api/v1/weather/current` | Current weather conditions |
| `GET` | `/api/v1/incidents` | Active incidents |
| `GET` | `/api/v1/cameras/feed` | Traffic camera feeds |
| `WS`  | `/ws/live` | Real-time WebSocket updates |

---

## 📊 Key Features

- **Real-time congestion forecasting** with confidence intervals
- **Multimodal reasoning** combining numeric, spatial, visual, and textual data
- **Explainable AI** — every prediction comes with a "why" (SHAP + LLM narrative)
- **What-if simulation** — test policy interventions before deploying
- **Multi-agent orchestration** — specialized LangGraph agents per domain
- **Map-first UX** — heatmaps, risk overlays, timeline playback
- **Production-grade MLOps** — model registry, A/B testing, drift detection
- **Event-driven architecture** — real-time data flow via Kafka
- **Horizontal scalability** — Kubernetes-native microservices

---

## ⚙️ Configuration

All configuration is done via environment variables. Copy `.env.example` to `.env` and fill in your values:

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for LLM agents | Yes |
| `MAPBOX_ACCESS_TOKEN` | Mapbox token for map rendering | Yes |
| `OPENWEATHERMAP_API_KEY` | Weather data API key | Yes |
| `POSTGRES_HOST` | PostgreSQL host | No (default: localhost) |
| `POSTGRES_PORT` | PostgreSQL port | No (default: 5432) |
| `REDIS_HOST` | Redis host | No (default: localhost) |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka broker address | No (default: localhost:9092) |

See [.env.example](.env.example) for the full list of configuration options.

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:

- Code style and standards
- Pull request process
- Issue reporting
- Development workflow

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
