from datetime import UTC, datetime
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from src.db.models.person import Person
from src.db.repositories.person_repository import PersonRepository


@pytest.mark.asyncio
async def test_create_person() -> None:
    """Проверка создания пользователя в репозитории."""

    mock_session = AsyncMock()
    mock_session.add_all = MagicMock()

    repository = PersonRepository(mock_session)
    person = Person(
        id=str(uuid4()),
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


@pytest.mark.asyncio
async def test_get_person_by_id_repository() -> None:
    """Проверка получения пользователя по ID из репозитория."""

    mock_session = AsyncMock()
    target_id = str(uuid4())
    mock_person = Person(id=target_id, first_name="John")

    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_person
    mock_session.execute.return_value = mock_result

    repository = PersonRepository(mock_session)
    result = await repository.get_by_id(target_id)

    assert result == mock_person
    mock_session.execute.assert_called_once()


@pytest.mark.asyncio
async def test_get_paginated_repository() -> None:
    """Проверка получения пагинированного списка пользователей из репозитория."""

    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_scalars = MagicMock()
    mock_scalars.all.return_value = []
    mock_result.scalars.return_value = mock_scalars
    mock_session.execute.return_value = mock_result

    repository = PersonRepository(mock_session)
    result = await repository.get_paginated(limit=10, offset=0)

    assert result == []
    mock_session.execute.assert_called_once()
