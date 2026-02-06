import json
from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator
from typing import List, Optional

from app.models.animal import (
    AnimalAdoptionStatus,
    AnimalAgeUnit,
    AnimalCurrentLocation,
    AnimalGender,
    AnimalSpecies,
    AnimalSize,
)


class AnimalCreate(BaseModel):
    name: str
    primary_photo_url: Optional[str] = None
    extra_photos_url: Optional[str] = None
    species: AnimalSpecies
    breed: Optional[str] = None
    size: Optional[AnimalSize] = None
    age: int
    age_unit: AnimalAgeUnit
    gender: AnimalGender
    adoption_status: Optional[AnimalAdoptionStatus] = AnimalAdoptionStatus.AVAILABLE
    current_location: Optional[AnimalCurrentLocation] = None
    description: Optional[str] = None
    medical_notes: Optional[str] = None
    behavioral_notes: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if len(v.strip()) < 2:
            raise ValueError("Name must be at least 2 characters")
        return v.strip()

    @field_validator("age")
    @classmethod
    def validate_age(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Age must be positive")
        if v > 50:
            raise ValueError("Age seems unrealistic (max 50)")
        return v

    @field_validator("primary_photo_url")
    @classmethod
    def validate_photo_url(cls, v: Optional[str]) -> Optional[str]:
        if v and not v.startswith(("http://", "https://")):
            raise ValueError("Photo URL must start with http:// or https://")
        return v

    @field_validator("extra_photos_url")
    @classmethod
    def validate_extra_photos(cls, v: Optional[str]) -> Optional[str]:
        if v:
            try:
                photos = json.loads(v)
                if not isinstance(photos, list):
                    raise ValueError("Extra photos must be a JSON array")

                for url in photos:
                    if not isinstance(url, str):
                        raise ValueError("All photo URLs must be strings")
                    if not url.startswith(("http://", "https://")):
                        raise ValueError("All photo URLs must start with http:// or https://")
            except json.JSONDecodeError:
                raise ValueError("Extra photos must be valid JSON")
        return v


class AnimalUpdate(BaseModel):
    name: Optional[str]
    primary_photo_url: Optional[str] = None
    extra_photos_url: Optional[str] = None
    species: Optional[AnimalSpecies]
    breed: Optional[str]
    size: Optional[AnimalSize]
    age: Optional[int]
    age_unit: Optional[AnimalAgeUnit]
    gender: Optional[AnimalGender]
    adoption_status: Optional[AnimalAdoptionStatus]
    current_location: Optional[AnimalCurrentLocation]
    description: Optional[str]
    medical_notes: Optional[str]
    behavioral_notes: Optional[str]

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if len(v.strip()) < 2:
            raise ValueError("Name must be at least 2 characters")
        return v.strip()

    @field_validator("age")
    @classmethod
    def validate_age(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("Age must be positive")
        if v > 100:
            raise ValueError("Age seems unrealistic (max 100)")
        return v

    @field_validator("primary_photo_url")
    @classmethod
    def validate_photo_url(cls, v: Optional[str]) -> Optional[str]:
        if v and not v.startswith(("http://", "https://")):
            raise ValueError("Photo URL must start with http:// or https://")
        return v

    @field_validator("extra_photos_url")
    @classmethod
    def validate_extra_photos(cls, v: Optional[str]) -> Optional[str]:
        if v:
            try:
                photos = json.loads(v)
                if not isinstance(photos, list):
                    raise ValueError("Extra photos must be a JSON array")

                for url in photos:
                    if not isinstance(url, str):
                        raise ValueError("All photo URLs must be strings")
                    if not url.startswith(("http://", "https://")):
                        raise ValueError("All photo URLs must start with http:// or https://")
            except json.JSONDecodeError:
                raise ValueError("Extra photos must be valid JSON")
        return v


class AnimalResponse(BaseModel):
    id: int
    name: str
    primary_photo_url: Optional[str] = None
    extra_photos_url: Optional[str] = None
    species: AnimalSpecies
    breed: Optional[str]
    size: Optional[AnimalSize]
    age: int
    age_unit: AnimalAgeUnit
    gender: AnimalGender
    adoption_status: Optional[AnimalAdoptionStatus]
    current_location: Optional[AnimalCurrentLocation]
    description: Optional[str]
    medical_notes: Optional[str]
    behavioral_notes: Optional[str]
    created_by_id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)


class PaginatedAnimalResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: List[AnimalResponse]


class AnimalFileUrl(BaseModel):
    url: str
