from fastapi import APIRouter

from src.api.people import router as people_router


api_router = APIRouter()
api_router.include_router(people_router)
