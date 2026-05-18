from abc import ABC, abstractmethod


class IRandomDataClient(ABC):
    """Интерфейс клиента random data API."""

    @abstractmethod
    async def get_people(
        self,
        count: int,
    ) -> list[dict]:
        """Получить список пользователей."""
