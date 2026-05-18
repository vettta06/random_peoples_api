from abc import ABC, abstractmethod

from src.db.models.person import Person


class IPeopleService(ABC):
    """Интерфейс сервиса пользователей."""

    @abstractmethod
    async def load_initial_people(
        self,
        count: int,
    ) -> None:
        """Загрузить начальный список пользователей."""

    @abstractmethod
    async def get_person(
        self,
        person_id: str,
    ) -> Person:
        """Получить пользователя по идентификатору."""

    @abstractmethod
    async def get_random_person(self) -> Person:
        """Получить случайного пользователя."""

    @abstractmethod
    async def get_people(
        self,
        page: int,
        size: int,
    ) -> list[Person]:
        """Получить список пользователей."""
