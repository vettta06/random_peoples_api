from unittest.mock import AsyncMock

import pytest

from src.db.models.person import Person
from src.services.people_service import PeopleService


@pytest.mark.asyncio
async def test_load_initial_people() -> None:
    """Проверить загрузку начального списка пользователей."""

    mock_raw_data = [
        {
            "Gender": "male",
            "FirstName": "John",
            "LastName": "Doe",
            "Phone": "+123456789",
            "Email": "john@example.com",
            "City": "Amsterdam",
        }
    ]
    mock_repository = AsyncMock()
    mock_client = AsyncMock()
    mock_client.get_people.return_value = mock_raw_data
    service = PeopleService(
        repository=mock_repository,
        client=mock_client,
    )
    await service.load_initial_people(count=1)
    mock_client.get_people.assert_called_once_with(1)
    mock_repository.create_many.assert_called_once()
    called_args = mock_repository.create_many.call_args[0][0]

    assert len(called_args) == 1
    assert isinstance(called_args[0], Person)
    assert called_args[0].first_name == "John"
    assert called_args[0].email == "john@example.com"
