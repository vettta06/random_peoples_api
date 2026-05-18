from abc import ABC
from abc import abstractmethod


class IRandomDataClient(ABC):
    """Интерфейс клиента random data API."""

    @abstractmethod
    async def get_people(
        self,
        count: int,
    ) -> list[dict]:
        """Получить список пользователей."""
