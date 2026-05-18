from datetime import datetime
from uuid import uuid4

import pytest

from src.db.models.person import Person
from src.db.repositories.person_repository import (
    PersonRepository,
)
from src.db.session import AsyncSessionLocal


@pytest.mark.asyncio
async def test_create_person() -> None:
    """Проверка создания пользователя."""

    async with AsyncSessionLocal() as session:
        repository = PersonRepository(session)
        person = Person(
            id=uuid4(),
            gender="male",
            first_name="John",
            last_name="Doe",
            phone="+123456789",
            email="john@example.com",
            city="Amsterdam",
            created_at=datetime.utcnow(),
        )
        await repository.create_many([person])

        saved_person = await repository.get_by_id(
            str(person.id),
        )

        assert saved_person is not None
        assert saved_person.email == person.email
