from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.person import Person
from src.db.repositories.interfaces.person import (
    IPersonRepository,
)


class PersonRepository(IPersonRepository):
    """Репозиторий пользователей."""

    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        """Инициализировать репозиторий."""

        self._session = session

    async def create_many(
        self,
        people: list[Person],
    ) -> None:
        """Создать пользователей."""

        self._session.add_all(people)
        await self._session.commit()

    async def get_by_id(
        self,
        person_id: str,
    ) -> Person | None:
        """Получить пользователя по идентификатору."""

        query = select(Person).where(Person.id == UUID(person_id))
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def get_random(self) -> Person | None:
        """Получить случайного пользователя."""

        query = select(Person).order_by(func.random()).limit(1)
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def get_paginated(
        self,
        limit: int,
        offset: int,
    ) -> list[Person]:
        """Получить список пользователей."""

        query = select(Person).limit(limit).offset(offset)
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def count(self) -> int:
        """Получить количество пользователей."""

        query = select(func.count(Person.id))
        result = await self._session.execute(query)
        return int(result.scalar_one())
