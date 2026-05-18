from datetime import UTC, datetime
from uuid import uuid4

import structlog

from src.db.models.person import Person
from src.db.repositories.interfaces.person import (
    IPersonRepository,
)
from src.exceptions import PersonNotFoundError
from src.services.interfaces.people_service import (
    IPeopleService,
)
from src.services.interfaces.random_data_client import (
    IRandomDataClient,
)

logger = structlog.get_logger(__name__)


class PeopleService(IPeopleService):
    """Сервис пользователей."""

    def __init__(
        self,
        repository: IPersonRepository,
        client: IRandomDataClient,
    ) -> None:
        """Инициализировать сервис."""

        self._repository = repository
        self._client = client

    async def load_initial_people(
        self,
        count: int,
    ) -> None:
        """Загрузить начальный список пользователей."""

        logger.info(
            "load_initial_people_started",
            count=count,
        )

        raw_people = await self._client.get_people(count)
        db_people = [
            Person(
                id=uuid4(),
                gender=item.get("Gender", ""),
                first_name=item.get("FirstName", ""),
                last_name=item.get("LastName", ""),
                phone=item.get("Phone", ""),
                email=item.get("Email", ""),
                city=item.get("City", ""),
                created_at=datetime.now(UTC),
            )
            for item in raw_people
        ]

        await self._repository.create_many(db_people)

        logger.info(
            "load_initial_people_finished",
            count=len(db_people),
        )

    async def get_person(
        self,
        person_id: str,
    ) -> Person:
        """Получить пользователя по идентификатору."""

        person = await self._repository.get_by_id(person_id)
        if person is None:
            logger.warning(
                "person_not_found",
                person_id=person_id,
            )
            raise PersonNotFoundError()
        return person

    async def get_random_person(self) -> Person:
        """Получить случайного пользователя."""

        person = await self._repository.get_random()
        if person is None:
            logger.warning("random_person_not_found")
            raise PersonNotFoundError()
        return person

    async def get_people(
        self,
        page: int,
        size: int,
    ) -> list[Person]:
        """Получить список пользователей."""

        offset = (page - 1) * size
        return await self._repository.get_paginated(
            limit=size,
            offset=offset,
        )
