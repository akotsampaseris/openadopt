from fastapi import APIRouter, Depends, HTTPException, Query
from logging import getLogger

from app.api.dependencies import require_admin
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User, UserRole
from app.schemas.animal import (
    AnimalCreate, 
    AnimalUpdate, 
    AnimalResponse,
    PaginatedAnimalResponse,
)
from app.services.animal_service import AnimalService

logger = getLogger(__name__)

router = APIRouter(prefix="/admin/animals")

@router.get("/", tags=["admin", "animals"], response_model=PaginatedAnimalResponse, status_code=200)
async def get_animals(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=settings.DEFAULT_PAGE_SIZE, le=settings.MAX_PAGE_SIZE),
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    try:
        total = await AnimalService.count_animals(db, current_user)
        animals = await AnimalService.get_animals(db, current_user, skip, limit)
        logger.info(f"Fetching animals for user with id {current_user.id}")
    except Exception as e:
        logger.warning(f"Error fetching animals: {e}")
        raise HTTPException(
            status_code=400, detail=f"Error fetching animals: {e}"
        )
    logger.info("Successfully fetched animals")
    
    return PaginatedAnimalResponse(
        items=animals,
        total=total,
        skip=skip,
        limit=limit
    )


@router.post("/", tags=["admin", "animals"], response_model=AnimalResponse, status_code=201)
async def create_animal(
    animal_data: AnimalCreate,
    current_user: User = Depends(require_admin),
    db = Depends(get_db),
):
    try:
        animal = await AnimalService.create_animal(db, animal_data, current_user)
        logger.info("Creating animal")
    except Exception as e:
        logger.warning(f"Error creating animal: {e}")
        raise HTTPException(
            status_code=400, detail=f"Error creating animal: {e}"
        )
    logger.info("Successfully created animal")

    return animal

@router.get("/{animal_id}", tags=["admin", "animals"], response_model=AnimalResponse, status_code=200)
async def get_animal(
    animal_id: int,
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):  
    try:
        animal = await AnimalService.get_animal_by_id(db, animal_id)
        logger.info(f"Fetching animal with id {animal_id}")
    except Exception as e:
        logger.warning(f"Error fetching animal with id {animal_id}: {e}")
        raise HTTPException(
            status_code=400, detail=f"Error fetching animal with id {animal_id}: {e}"
        )
    logger.info(f"Successfuly fetched animal with id {animal_id}")

    if not animal:
        raise HTTPException(
            status_code=404, 
            detail="Animal not found!"
        )
    
    if (
        current_user.role != UserRole.SUPER_ADMIN 
        and current_user.id != animal.created_by_id
    ):
        logger.warning(f"Access to animal with id {animal_id} not allowed")
        raise HTTPException(
            status_code=401, 
            detail=f"Access to animal with id {animal_id} not allowed"
        )
    
    return animal


@router.patch("/{animal_id}", tags=["admin", "animals"], response_model=AnimalResponse, status_code=200)
async def update_animal(
    animal_id: int,
    animal_data: AnimalUpdate,
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    try:
        animal = await AnimalService.get_animal_by_id(db, animal_id)
        logger.info(f"Fetching animal with id {animal_id}")
    except Exception as e:
        logger.warning(f"Error fetching animal with id {animal_id}: {e}")
        raise HTTPException(
            status_code=400, detail=f"Error fetching animal with id {animal_id}: {e}"
        )
    logger.info(f"Successfuly fetched animal with id {animal_id}")

    if not animal:
        logger.warning(f"Animal with id {animal_id} not found")
        raise HTTPException(
            status_code=404, 
            detail=f"Animal with id {animal_id} not found"
        )
    
    if (
        current_user.role != UserRole.SUPER_ADMIN 
        and current_user.id != animal.created_by_id
    ):
        logger.warning(f"Access to animal with id {animal_id} not allowed")
        raise HTTPException(
            status_code=401, 
            detail=f"Access to animal with id {animal_id} not allowed"
        )
    
    try:
        animal = await AnimalService.update_animal(db, animal, animal_data)
        logger.info(f"Updating animal with id {animal_id}")
    except Exception as e:
        logger.warning(f"Error updating animal with id {animal_id}: {e}")
        raise HTTPException(
            status_code=400, 
            detail=f"Error updating animal with id {animal_id}: {e}"
        )
    logger.info(f"Successfully updated animal with id {animal_id}")
    
    return animal


@router.delete("/{animal_id}", tags=["admin", "animals"], status_code=204)
async def delete_animal(
    animal_id: int,
    current_user: User = Depends(require_admin),
    db = Depends(get_db)
):
    try:
        animal = await AnimalService.get_animal_by_id(db, animal_id)
        logger.info(f"Fetching animal with id {animal_id}")
    except Exception as e:
        logger.warning(f"Error fetching animal with id {animal_id}: {e}")
        raise HTTPException(
            status_code=400, detail=f"Error fetching animal with id {animal_id}: {e}"
        )
    logger.info(f"Successfuly fetched animal with id {animal_id}")

    if not animal:
        logger.warning(f"Animal with id {animal_id} not found")
        raise HTTPException(
            status_code=404, 
            detail=f"Animal with id {animal_id} not found"
        )
    
    if (
        current_user.role != UserRole.SUPER_ADMIN 
        and current_user.id != animal.created_by_id
    ):
        logger.warning(f"Access to animal with id {animal_id} not allowed")
        raise HTTPException(
            status_code=401, 
            detail=f"Access to animal with id {animal_id} not allowed"
        )

    try:
        await AnimalService.delete_animal(db, animal)
        logger.info(f"Deleting animal with id {animal_id}")
    except Exception as e:
        logger.warning(f"Error deleting animal with id {animal_id}: {e}")
        raise HTTPException(
            status_code=400, 
            detail=f"Error deleting animal with id {animal_id}: {e}"
        )
    logger.info(f"Successfully deleted animal with id {animal_id}")
    
    return 