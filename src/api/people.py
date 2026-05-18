from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query
from fastapi import status

from src.api.dependencies import get_people_service
from src.exceptions import PersonNotFoundError
from src.schemas.person import Person as PersonSchema
from src.services.people_service import PeopleService


router = APIRouter(tags=["People"])


@router.get(
    "/",
    response_model=list[PersonSchema],
)
async def get_people(
    page: int = Query(default=1, ge=1, description="Номер страницы"),
    size: int = Query(default=50, ge=1, le=100, description="Размер страницы"),
    service: PeopleService = Depends(get_people_service),
) -> list[PersonSchema]:
    """Получить список пользователей с поддержкой пагинации."""

    db_people = await service.get_people(page=page, size=size)
    return [PersonSchema.model_validate(person) for person in db_people]


@router.get(
    "/random",
    response_model=PersonSchema,
)
async def get_random_person(
    service: PeopleService = Depends(get_people_service),
) -> PersonSchema:
    """Получить случайного пользователя."""

    try:
        db_person = await service.get_random_person()
        return PersonSchema.model_validate(db_person)
    except PersonNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="People database is empty",
        )


@router.get(
    "/users/{user_id}",
    response_model=PersonSchema,
)
async def get_person_by_id(
    user_id: str,
    service: PeopleService = Depends(get_people_service),
) -> PersonSchema:
    """Получить пользователя по идентификатору."""

    try:
        db_person = await service.get_person(user_id)
        return PersonSchema.model_validate(db_person)
    except PersonNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Person not found",
        )
