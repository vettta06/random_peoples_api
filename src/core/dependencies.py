from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import AsyncSessionLocal


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Получить сессию базы данных."""

    async with AsyncSessionLocal() as session:
        yield session
