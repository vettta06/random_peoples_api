from fastapi import FastAPI

from src.core.config import config
from src.core.logging import configure_logging


configure_logging()
app = FastAPI(title=config.app_name)


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    """Проверка состояния приложения."""

    return {"status": "ok"}
