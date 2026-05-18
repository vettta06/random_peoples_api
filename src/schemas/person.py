from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import EmailStr


class Person(BaseModel):
    """Схема пользователя."""
    id: UUID
    gender: str
    first_name: str
    last_name: str
    phone: str
    email: EmailStr
    city: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
