from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["health"])
async def get_health():
    return [{"status": "oknot"}]