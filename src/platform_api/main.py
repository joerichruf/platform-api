from importlib.metadata import version
from fastapi import FastAPI
from .routers import health

def create_app() -> FastAPI:
    app = FastAPI(
        title="Platform API",
        version=version("platform-api"),
    )
    return app

app = create_app()
app.include_router(health.router)