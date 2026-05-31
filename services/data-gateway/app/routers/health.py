from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    return {"status": "healthy", "service": "data-gateway"}


@router.get("/ready")
async def readiness_check():
    # TODO: Check database, kafka, redis connectivity
    return {"status": "ready"}
