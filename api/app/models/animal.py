from enum import StrEnum
from sqlalchemy import ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Text
from typing import Optional

from app.core.database import Base


class AnimalGender(StrEnum):
    MALE = "male"
    FEMALE = "female"


class AnimalAgeUnit(StrEnum):
    MONTHS = "months"
    YEARS = "years"


class AnimalAdoptionStatus(StrEnum):
    AVAILABLE = "available"
    ADOPTED = "adopted"
    ON_HOLD = "on_hold"


class AnimalSpecies(StrEnum):
    DOG = "dog"
    CAT = "cat"
    OTHER = "other"


class AnimalSize(StrEnum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class AnimalCurrentLocation(StrEnum):
    FOSTERED = "fostered"
    SHELTER = "shelter"
    STRAY = "stray"


class Animal(Base):
    __tablename__ = "animals"

    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_by: Mapped["User"] = relationship(back_populates="animals")  # noqa
    name: Mapped[str]
    primary_photo_url: Mapped[Optional[str]] = mapped_column(default=None)
    extra_photos_url: Mapped[Optional[str]] = mapped_column(Text, default=None)
    species: Mapped[AnimalSpecies] = mapped_column(SQLEnum(AnimalSpecies))
    breed: Mapped[Optional[str]]
    size: Mapped[Optional[AnimalSize]] = mapped_column(
        SQLEnum(AnimalSize), default=None, nullable=True
    )
    age: Mapped[int]
    age_unit: Mapped[AnimalAgeUnit] = mapped_column(SQLEnum(AnimalAgeUnit))
    gender: Mapped[AnimalGender] = mapped_column(SQLEnum(AnimalGender))
    adoption_status: Mapped[AnimalAdoptionStatus] = mapped_column(
        SQLEnum(AnimalAdoptionStatus), default=AnimalAdoptionStatus.AVAILABLE
    )
    current_location: Mapped[Optional[AnimalCurrentLocation]] = mapped_column(
        SQLEnum(AnimalCurrentLocation), default=None, nullable=True
    )
    description: Mapped[Optional[str]] = mapped_column(Text, default=None)
    medical_notes: Mapped[Optional[str]] = mapped_column(Text, default=None)
    behavioral_notes: Mapped[Optional[str]] = mapped_column(Text, default=None)
