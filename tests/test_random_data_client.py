from unittest.mock import AsyncMock, patch

import pytest

from src.services.random_data_client import RandomDataClient


@pytest.mark.asyncio
async def test_get_people() -> None:
    """Проверить получение пользователей."""

    mock_data = [{"FirstName": "John"}]
    client = RandomDataClient()
    with patch.object(
        client, "get_people", new_callable=AsyncMock, return_value=mock_data
    ):
        people = await client.get_people(1)
        assert len(people) == 1
        assert people[0]["FirstName"] == "John"
