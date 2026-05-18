from abc import ABC
from abc import abstractmethod

from src.db.models.person import Person


class IPersonRepository(ABC):
    """Интерфейс репозитория пользователей."""

    @abstractmethod
    async def create_many(
        self,
        people: list[Person],
    ) -> None:
        """Создать пользователей."""

    @abstractmethod
    async def get_by_id(
        self,
        person_id: str,
    ) -> Person | None:
        """Получить пользователя по идентификатору."""

    @abstractmethod
    async def get_random(self) -> Person | None:
        """Получить случайного пользователя."""

    @abstractmethod
    async def get_paginated(
        self,
        limit: int,
        offset: int,
    ) -> list[Person]:
        """Получить список пользователей."""

    @abstractmethod
    async def count(self) -> int:
        """Получить количество пользователей."""
