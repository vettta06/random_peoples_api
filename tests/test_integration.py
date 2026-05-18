from unittest.mock import AsyncMock

from fastapi import status
from fastapi.testclient import TestClient
import pytest

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
