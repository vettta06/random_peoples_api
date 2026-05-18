from datetime import datetime
from unittest.mock import AsyncMock

from fastapi import HTTPException
import pytest

from src.api.people import get_people
from src.api.people import get_person_by_id
from src.api.people import get_random_person
from src.db.models.person import Person
from src.exceptions import PersonNotFoundError


@pytest.mark.asyncio
async def test_get_people_endpoint_success() -> None:
    """Проверка успешного возврата списка пользователей эндпоинтом."""

    mock_service = AsyncMock()
    mock_service.get_people.return_value = [
        Person(
            id="fc90ee35-b008-4e9a-8b9a-04f3b220e92a",
            gender="male",
            first_name="John",
            last_name="Doe",
            phone="+123456789",
            email="john@example.com",
            city="Amsterdam",
            created_at=datetime.now(),
        )
    ]
    result = await get_people(page=2, size=20, service=mock_service)

    assert len(result) == 1
    assert result[0].first_name == "John"
    mock_service.get_people.assert_called_once_with(page=2, size=20)


@pytest.mark.asyncio
async def test_get_random_person_endpoint_success() -> None:
    """Проверка успешного возврата случайного пользователя эндпоинтом."""

    mock_service = AsyncMock()
    mock_service.get_random_person.return_value = Person(
        id="fc90ee35-b008-4e9a-8b9a-04f3b220e92a",
        gender="male",
        first_name="John",
        last_name="Doe",
        phone="+123456789",
        email="john@example.com",
        city="Amsterdam",
        created_at=datetime.now(),
    )

    result = await get_random_person(service=mock_service)

    assert result.first_name == "John"
    mock_service.get_random_person.assert_called_once()


@pytest.mark.asyncio
async def test_get_person_by_id_endpoint_success() -> None:
    """Проверка успешного возврата пользователя по идентификатору."""

    target_id = "fc90ee35-b008-4e9a-8b9a-04f3b220e92a"
    mock_service = AsyncMock()
    mock_service.get_person.return_value = Person(
        id=target_id,
        gender="male",
        first_name="John",
        last_name="Doe",
        phone="+123456789",
        email="john@example.com",
        city="Amsterdam",
        created_at=datetime.now(),
    )

    result = await get_person_by_id(user_id=target_id, service=mock_service)

    assert str(result.id) == target_id
    mock_service.get_person.assert_called_once_with(target_id)


@pytest.mark.asyncio
async def test_get_person_by_id_endpoint_not_found() -> None:
    """Проверка генерации ошибки 404, если пользователь не найден."""

    target_id = "00000000-0000-0000-0000-000000000000"
    mock_service = AsyncMock()
    mock_service.get_person.side_effect = PersonNotFoundError()

    with pytest.raises(HTTPException) as exc_info:
        await get_person_by_id(user_id=target_id, service=mock_service)

    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Person not found"
