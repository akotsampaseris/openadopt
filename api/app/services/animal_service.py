from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models.animal import Animal
from app.models.user import User, UserRole


class AnimalService:
    @staticmethod
    async def count_animals(db: AsyncSession, user: User = None):
        stmt = select(func.count()).select_from(Animal)

        if user and user.role == UserRole.ADMIN:
            # If the authenticated user is an admin,
            # the query should return only animals created by that user.
            # That will be used only in an admin view of the animals.
            # In a public view all animals will be returned.
            stmt = stmt.where(Animal.created_by_id==user.id)

        total = await db.scalar(stmt)

        return total


    @staticmethod
    async def get_animals(
        db: AsyncSession, user: User = None, skip: int = 0, limit: int = 50
    ) -> List[Animal]:
        stmt = select(Animal)

        if user and user.role == UserRole.ADMIN:
            # If the authenticated user is an admin,
            # the query should return only animals created by that user.
            # That will be used only in an admin view of the animals.
            # In a public view all animals will be returned.
            stmt = stmt.where(Animal.created_by_id==user.id)
        
        stmt = stmt.offset(skip).limit(limit)
        result = await db.scalars(stmt)

        animals = result.all()

        return animals
    
    @staticmethod
    async def get_animal_by_id(db: AsyncSession, id: int) -> Animal:
        stmt = select(Animal).where(Animal.id == id)
        result = await db.execute(stmt)

        animal = result.scalar_one_or_none()
        
        return animal
    
    @staticmethod
    async def create_animal(db: AsyncSession, animal_data: dict, user: User) -> Animal:
        animal = Animal(
            name=animal_data.name,
            primary_photo_url=animal_data.primary_photo_url,
            extra_photos_url=animal_data.extra_photos_url,
            species=animal_data.species,
            breed=animal_data.breed,
            size=animal_data.size,
            age=animal_data.age,
            age_unit=animal_data.age_unit,
            gender=animal_data.gender,
            adoption_status=animal_data.adoption_status,
            current_location=animal_data.current_location,
            description=animal_data.description,
            medical_notes=animal_data.medical_notes,
            behavioral_notes=animal_data.behavioral_notes,
            created_by_id=user.id
        )
        
        db.add(animal)
        await db.commit()

        return animal
    
    @staticmethod
    async def update_animal(
        db: AsyncSession, animal: Animal, animal_data: dict
    ) -> Animal:
        # Partial update of the animal's attributes
        updated_data = animal_data.model_dump(exclude_unset=True)
        for field, value in updated_data.items():
            setattr(animal, field, value)
        
        await db.commit()
        await db.refresh(animal)

        return animal
    
    @staticmethod
    async def delete_animal(db: AsyncSession, animal: Animal) -> None:
        await db.delete(animal)        
        await db.commit()
        
        return
