from fastapi import APIRouter, Query, UploadFile, File

router = APIRouter()


@router.get("/feeds")
async def get_camera_feeds():
    """List available camera feeds."""
    return {"cameras": []}


@router.get("/snapshot/{camera_id}")
async def get_camera_snapshot(camera_id: str):
    """Get latest snapshot from a camera."""
    return {"camera_id": camera_id, "snapshot_url": None, "analysis": None}


@router.post("/analyze")
async def analyze_camera_frame(file: UploadFile = File(...)):
    """Analyze a traffic camera frame for vehicle density and incidents."""
    # TODO: Send to vision model inference service
    return {
        "filename": file.filename,
        "vehicle_count": 0,
        "congestion_class": "unknown",
        "incidents_detected": [],
    }
