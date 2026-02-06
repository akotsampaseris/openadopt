from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models.animal import Animal
from app.models.user import User, UserRole


class AnimalService:
    @staticmethod
    async def count_animals(db: AsyncSession, user: User | None = None):
        stmt = select(func.count()).select_from(Animal)

        if user and user.role == UserRole.ADMIN:
            # If the authenticated user is an admin,
            # the query should return only animals created by that user.
            # That will be used only in an admin view of the animals.
            # In a public view all animals will be returned.
            stmt = stmt.where(Animal.created_by_id == user.id)

        total = await db.scalar(stmt)

        return total

    @staticmethod
    async def get_animals(
        db: AsyncSession, user: User | None = None, skip: int = 0, limit: int = 50
    ) -> List[Animal]:
        stmt = select(Animal)

        if user and user.role == UserRole.ADMIN:
            # If the authenticated user is an admin,
            # the query should return only animals created by that user.
            # That will be used only in an admin view of the animals.
            # In a public view all animals will be returned.
            stmt = stmt.where(Animal.created_by_id == user.id)

        stmt = stmt.offset(skip).limit(limit)
        result = await db.scalars(stmt)

        animals = list(result.all())

        return animals

    @staticmethod
    async def get_animal_by_id(db: AsyncSession, id: int) -> Animal | None:
        stmt = select(Animal).where(Animal.id == id)
        result = await db.execute(stmt)

        animal = result.scalar_one_or_none()

        return animal

    @staticmethod
    async def create_animal(db: AsyncSession, animal_data: dict, user: User) -> Animal:
        animal = Animal(
            **animal_data,
            created_by_id=user.id,
        )

        db.add(animal)
        await db.commit()

        return animal

    @staticmethod
    async def update_animal(db: AsyncSession, animal: Animal, animal_data: dict) -> Animal:
        for field, value in animal_data.items():
            setattr(animal, field, value)

        await db.commit()
        await db.refresh(animal)

        return animal

    @staticmethod
    async def delete_animal(db: AsyncSession, animal: Animal) -> None:
        await db.delete(animal)
        await db.commit()

        return
