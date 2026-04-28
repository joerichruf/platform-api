from importlib.metadata import version
from fastapi import FastAPI
from .routers import health, deployments
from .configs import config

def create_app() -> FastAPI:
    settings = config.get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=version("platform-api"),
    )
    app.include_router(health.router)
    app.include_router(deployments.router)
    return app

app = create_app()