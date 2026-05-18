import structlog
from httpx import AsyncClient, HTTPError, Response, Timeout

from src.core.config import config
from src.services.interfaces.random_data_client import (
    IRandomDataClient,
)

logger = structlog.get_logger(__name__)


class RandomDataClient(IRandomDataClient):
    """Клиент random data API."""

    def __init__(self) -> None:
        """Инициализировать клиент."""

        self._client = AsyncClient(
            base_url=config.random_data_api_url,
            timeout=Timeout(30.0),
        )

    async def get_people(
        self,
        count: int,
    ) -> list[dict]:
        """Получить список пользователей."""

        logger.info(
            "request_random_people_started",
            count=count,
        )

        try:
            response = await self._client.get(
                "/",
                params={
                    "count": count,
                },
            )
            self._raise_for_status(response)
            data = response.json()
            logger.info(
                "request_random_people_finished",
                count=len(data),
            )
            return data

        except HTTPError as error:
            logger.error(
                "request_random_people_failed",
                error=str(error),
            )
            raise

    @staticmethod
    def _raise_for_status(
        response: Response,
    ) -> None:
        """Проверить статус ответа."""

        response.raise_for_status()
