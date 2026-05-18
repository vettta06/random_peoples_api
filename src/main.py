from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.api.router import api_router
from src.core.config import config
from src.core.logging import configure_logging
from src.startup.bootstrap import bootstrap_application


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Управление жизненным циклом приложения."""
    await bootstrap_application()
    yield


configure_logging()

app = FastAPI(
    title=config.app_name,
    lifespan=lifespan,
)

app.include_router(api_router)
