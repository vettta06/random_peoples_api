from datetime import UTC, datetime
from uuid import uuid4

import pytest

from src.db.models.person import Person
from src.db.repositories.person_repository import (
    PersonRepository,
)

from unittest.mock import AsyncMock


@pytest.mark.asyncio
async def test_create_person() -> None:
    """Проверка создания пользователя в репозитории."""

    mock_session = AsyncMock()
    repository = PersonRepository(mock_session)

    person = Person(
        id=uuid4(),
        gender="male",
        first_name="John",
        last_name="Doe",
        phone="+123456789",
        email="john@example.com",
        city="Amsterdam",
        created_at=datetime.now(UTC),
    )
    await repository.create_many([person])

    mock_session.add_all.assert_called_once_with([person])
    mock_session.commit.assert_called_once()
