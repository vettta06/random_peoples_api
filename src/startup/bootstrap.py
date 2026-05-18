import structlog

from src.db.repositories.person_repository import PersonRepository
from src.db.session import AsyncSessionLocal
from src.services.people_service import PeopleService
from src.services.random_data_client import RandomDataClient

logger = structlog.get_logger(__name__)


async def bootstrap_application() -> None:
    """Инициализировать начальные данные при старте приложения."""

    logger.info("application_bootstrap_started")

    async with AsyncSessionLocal() as session:
        repository = PersonRepository(session)
        client = RandomDataClient()
        service = PeopleService(repository, client)
        people_count = await repository.count()
        if people_count == 0:
            logger.info("database_is_empty_starting_initial_load")
            await service.load_initial_people(1000)
            logger.info("database_initial_load_finished")
        else:
            logger.info(
                "database_already_has_data_bootstrap_skipped",
                current_count=people_count,
            )
