from unittest.mock import AsyncMock

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.api.dependencies import get_people_service
from src.main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_people_service() -> AsyncMock:  # type: ignore[misc]
    """Создать мок для сервиса пользователей и внедрить его в FastAPI."""

    mock = AsyncMock()
    mock.get_people.return_value = []

    app.dependency_overrides[get_people_service] = lambda: mock
    yield mock
    app.dependency_overrides.clear()


def test_integration_get_people_pagination_defaults(
    mock_people_service: AsyncMock,
) -> None:
    """Проверка дефолтных параметров пагинации на главной странице."""

    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK

    mock_people_service.get_people.assert_called_once_with(page=1, size=50)


def test_integration_get_people_pagination_custom(
    mock_people_service: AsyncMock,
) -> None:
    """Проверка кастомных параметров пагинации с конкретным размером страницы."""

    response = client.get("/?page=2&size=5")
    assert response.status_code == status.HTTP_200_OK

    mock_people_service.get_people.assert_called_once_with(page=2, size=5)


def test_integration_get_people_pagination_invalid_size() -> None:
    """Проверка валидации некорректного размера страницы при превышении лимита."""

    response = client.get("/?size=150")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_integration_get_people_pagination_invalid_page() -> None:
    """Проверка Human-friendly валидации некорректного номера страницы."""

    response = client.get("/?page=0")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_integration_get_person_by_id_not_found(mock_people_service: AsyncMock) -> None:
    """Проверка валидации и возврата 404 если пользователь не найден."""

    from src.exceptions import PersonNotFoundError

    target_id = "00000000-0000-0000-0000-000000000000"
    mock_people_service.get_person.side_effect = PersonNotFoundError()

    response = client.get(f"/users/{target_id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Person not found"


def test_integration_get_person_by_id_success(mock_people_service: AsyncMock) -> None:
    """Проверка успешного получения пользователя по ID через API."""

    from datetime import datetime

    from src.db.models.person import Person

    target_id = "fc90ee35-b008-4e9a-8b9a-04f3b220e92a"
    mock_person = Person(
        id=target_id,
        gender="male",
        first_name="John",
        last_name="Doe",
        phone="+123456789",
        email="john@example.com",
        city="Amsterdam",
        created_at=datetime.now(),
    )
    mock_people_service.get_person.return_value = mock_person

    response = client.get(f"/users/{target_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == target_id
    mock_people_service.get_person.assert_called_once_with(target_id)


def test_integration_get_random_person_success(mock_people_service: AsyncMock) -> None:
    """Проверка успешного получения случайного пользователя через API."""

    from datetime import datetime

    from src.db.models.person import Person

    mock_person = Person(
        id="fc90ee35-b008-4e9a-8b9a-04f3b220e92a",
        gender="female",
        first_name="Jane",
        last_name="Doe",
        phone="+123456789",
        email="jane@example.com",
        city="Amsterdam",
        created_at=datetime.now(),
    )
    mock_people_service.get_random_person.return_value = mock_person

    response = client.get("/random")

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["first_name"] == "Jane"
    mock_people_service.get_random_person.assert_called_once()
