from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.repositories.person_repository import PersonRepository
from src.db.session import AsyncSessionLocal
from src.services.people_service import PeopleService
from src.services.random_data_client import RandomDataClient


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Получить сессию базы данных."""

    async with AsyncSessionLocal() as session:
        yield session


def get_people_service(
    session: AsyncSession = Depends(get_db_session),
) -> PeopleService:
    """Получить сервис пользователей."""

    repository = PersonRepository(session)
    client = RandomDataClient()
    return PeopleService(repository, client)
