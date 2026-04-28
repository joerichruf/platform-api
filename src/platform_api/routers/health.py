from fastapi import APIRouter, Depends
from ..configs.config import get_settings, Settings
from importlib.metadata import version

router = APIRouter()

@router.get("/health", tags=["health"])
async def get_health(settings: Settings = Depends(get_settings)):
    information = {}
    app_name = settings.app_name
    version_value = version("platform-api")
    information["app_name"] = app_name
    information["version"] = version_value
    information["status"] = "ok"
    return information