"""UrbanPulse AI - Data Gateway Service"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import health, traffic, transit, weather, incidents, cameras
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(f"🚀 UrbanPulse Data Gateway starting in {settings.environment} mode")
    yield
    # Shutdown
    print("👋 UrbanPulse Data Gateway shutting down")


app = FastAPI(
    title="UrbanPulse AI - Data Gateway",
    description="Real-time city data ingestion and serving API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router, tags=["Health"])
app.include_router(traffic.router, prefix="/api/v1/traffic", tags=["Traffic"])
app.include_router(transit.router, prefix="/api/v1/transit", tags=["Transit"])
app.include_router(weather.router, prefix="/api/v1/weather", tags=["Weather"])
app.include_router(incidents.router, prefix="/api/v1/incidents", tags=["Incidents"])
app.include_router(cameras.router, prefix="/api/v1/cameras", tags=["Cameras"])
