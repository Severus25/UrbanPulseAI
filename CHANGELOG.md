# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project scaffolding and architecture
- Data Gateway service with FastAPI (traffic, transit, weather, incidents, cameras endpoints)
- Inference service skeleton for ML model serving
- Orchestration service skeleton for LangGraph agent coordination
- Retrieval service skeleton for RAG-based document search
- Simulation service skeleton for what-if scenarios
- ML model modules: congestion forecasting, incident detection, ETA prediction, risk scoring, vision
- LangGraph agent modules: traffic reasoner, mobility planner, policy retrieval, simulation, narrative
- Feature store module for feature engineering pipelines
- Next.js 15 frontend with Mapbox GL, Deck.gl, and Zustand state management
- Dashboard component with AI panel and city map
- Apache Kafka integration for real-time data streaming
- Airflow DAGs for traffic and weather data ingestion
- Docker Compose setup with PostgreSQL/PostGIS, Redis, Kafka, MinIO, ChromaDB
- Kubernetes manifests and Terraform configuration
- Prometheus monitoring configuration
- GitHub Actions CI/CD pipeline
- Comprehensive documentation (architecture, API spec, deployment guide)
- Unit test framework with pytest
- Environment configuration via .env with example template

### Infrastructure
- PostgreSQL 16 with PostGIS for geospatial data
- Redis 7 for caching and rate limiting
- Apache Kafka for event streaming
- MinIO for S3-compatible object storage
- ChromaDB for vector embeddings

## [0.1.0] - 2024-01-15

### Added
- Initial release
- Project structure and architecture design
- Core service implementations
- Documentation suite

[Unreleased]: https://github.com/YOUR_USERNAME/UrbanPulse_AI/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/YOUR_USERNAME/UrbanPulse_AI/releases/tag/v0.1.0
