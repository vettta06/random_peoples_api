from uuid import UUID

from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.db.session import Base


class Person(Base):
    """Модель пользователя."""

    __tablename__ = "people"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    gender: Mapped[str] = mapped_column(String(20), nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at = mapped_column(
        DateTime(timezone=True),
    )
