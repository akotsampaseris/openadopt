import uuid
from logging import getLogger
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

from app.api.dependencies import require_admin
from app.core.config import settings
from app.core.database import get_db
from app.core.storage.factory import get_storage_backend
from app.models.user import User, UserRole
from app.schemas.animal import (
    AnimalCreate,
    AnimalFileUrl,
    AnimalResponse,
    AnimalUpdate,
    PaginatedAnimalResponse,
)
from app.services.animal_service import AnimalService

logger = getLogger(__name__)

router = APIRouter(prefix="/admin/animals")


# File upload constants
ALLOWED_FILE_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/webp",
    "image/gif",
    "video/mp4",
    "video/mpeg",
    "video/quicktime",
}
MAX_FILE_UPLOAD_SIZE = 6 * 1024 * 1024  # 5MB in bytes
MAX_FILES_PER_ANIMAL = 10


async def get_animal_and_authorize_access(db, animal_id: int, user: User):
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
        raise HTTPException(status_code=404, detail=f"Animal with id {animal_id} not found")

    if user.role != UserRole.SUPER_ADMIN and user.id != animal.created_by_id:
        logger.warning(f"Access to animal with id {animal_id} not allowed")
        raise HTTPException(
            status_code=401, detail=f"Access to animal with id {animal_id} not allowed"
        )

    return animal


def validate_file(
    file: UploadFile, allowed_types: set = ALLOWED_FILE_TYPES, max_size: int = MAX_FILE_UPLOAD_SIZE
) -> None:
    """Validate file type and size."""
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, detail=f"Invalid file type. Allowed: {', '.join(allowed_types)}"
        )

    # Check file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()  # Get position (size)
    file.file.seek(0)  # Reset to beginning

    if file_size > max_size:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {max_size / (1024 * 1024):.1f}MB",
        )


@router.get("/", tags=["admin", "animals"], response_model=PaginatedAnimalResponse, status_code=200)
async def get_animals(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=settings.DEFAULT_PAGE_SIZE, le=settings.MAX_PAGE_SIZE),
    current_user: User = Depends(require_admin),
    db=Depends(get_db),
):
    try:
        total = await AnimalService.count_animals(db, current_user)
        animals = await AnimalService.get_animals(db, current_user, skip, limit)
        logger.info(f"Fetching animals for user with id {current_user.id}")
    except Exception as e:
        logger.warning(f"Error fetching animals: {e}")
        raise HTTPException(status_code=400, detail=f"Error fetching animals: {e}")
    logger.info("Successfully fetched animals")

    animals = [AnimalResponse.model_validate(animal) for animal in animals]

    return PaginatedAnimalResponse(items=animals, total=total, skip=skip, limit=limit)


@router.post("/", tags=["admin", "animals"], response_model=AnimalResponse, status_code=201)
async def create_animal(
    animal_data: AnimalCreate,
    current_user: User = Depends(require_admin),
    db=Depends(get_db),
):
    try:
        animal = await AnimalService.create_animal(db, animal_data.model_dump(), current_user)
        logger.info("Creating animal")
    except Exception as e:
        logger.warning(f"Error creating animal: {e}")
        raise HTTPException(status_code=400, detail=f"Error creating animal: {e}")
    logger.info("Successfully created animal")

    return animal


@router.get(
    "/{animal_id}", tags=["admin", "animals"], response_model=AnimalResponse, status_code=200
)
async def get_animal(
    animal_id: int, current_user: User = Depends(require_admin), db=Depends(get_db)
):
    animal = await get_animal_and_authorize_access(db, animal_id, current_user)

    return animal


@router.patch(
    "/{animal_id}", tags=["admin", "animals"], response_model=AnimalResponse, status_code=200
)
async def update_animal(
    animal_id: int,
    animal_data: AnimalUpdate,
    current_user: User = Depends(require_admin),
    db=Depends(get_db),
):
    animal = await get_animal_and_authorize_access(db, animal_id, current_user)

    try:
        animal = await AnimalService.update_animal(
            db, animal, animal_data.model_dump(exclude_unset=True)
        )
        logger.info(f"Updating animal with id {animal_id}")
    except Exception as e:
        logger.warning(f"Error updating animal with id {animal_id}: {e}")
        raise HTTPException(
            status_code=400, detail=f"Error updating animal with id {animal_id}: {e}"
        )
    logger.info(f"Successfully updated animal with id {animal_id}")

    return animal


@router.delete("/{animal_id}", tags=["admin", "animals"], status_code=204)
async def delete_animal(
    animal_id: int,
    storage=Depends(get_storage_backend),
    current_user: User = Depends(require_admin),
    db=Depends(get_db),
):
    animal = await get_animal_and_authorize_access(db, animal_id, current_user)

    try:
        await AnimalService.delete_animal(db, animal)
        await storage.delete_dir(f"animals/{animal_id}")
        logger.info(f"Deleting animal with id {animal_id}")
    except Exception as e:
        logger.warning(f"Error deleting animal with id {animal_id}: {e}")
        raise HTTPException(
            status_code=400, detail=f"Error deleting animal with id {animal_id}: {e}"
        )
    logger.info(f"Successfully deleted animal with id {animal_id}")

    return


@router.post("/{animal_id}/photos/primary", status_code=201, response_model=AnimalFileUrl)
async def upload_animal_primary_photo(
    animal_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(require_admin),
    storage=Depends(get_storage_backend),
    db=Depends(get_db),
):
    animal = await get_animal_and_authorize_access(db, animal_id, current_user)

    # Validate file
    validate_file(file)

    # Generate unique filename
    file_ext = Path(file.filename).suffix
    filename = f"{uuid.uuid4()}{file_ext}"
    file_path = f"animals/{animal_id}/files/{filename}"

    # Upload file
    try:
        file_url = await storage.upload_file(file, file_path)
    except Exception as e:
        logger.warning(f"File was not uploaded: {e}")
        raise HTTPException(status_code=400, detail=f"File was not uploaded: {e}")

    # Assign the new primary photo
    old_primary_photo_url = animal.primary_photo_url
    animal.primary_photo_url = file_url

    await db.commit()
    await db.refresh(animal)

    if old_primary_photo_url:
        try:
            await storage.delete_file(old_primary_photo_url)
        except Exception as e:
            logger.warning(f"File {old_primary_photo_url} could not be deleted: {e}")

    return {"url": file_url}


@router.post("/{animal_id}/files", status_code=201, response_model=AnimalFileUrl)
async def upload_animal_file(
    animal_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(require_admin),
    storage=Depends(get_storage_backend),
    db=Depends(get_db),
):
    animal = await get_animal_and_authorize_access(db, animal_id, current_user)

    # Validate file
    validate_file(file)

    # Generate unique filename
    file_ext = Path(file.filename).suffix
    filename = f"{uuid.uuid4()}{file_ext}"
    file_path = f"animals/{animal_id}/files/{filename}"

    import json

    animal_files = json.loads(animal.extra_photos_url) if animal.extra_photos_url else []

    if len(animal_files) >= MAX_FILES_PER_ANIMAL:
        raise HTTPException(status_code=400, detail=f"Maximum {MAX_FILES_PER_ANIMAL} files allowed")

    # Upload file
    try:
        file_url = await storage.upload_file(file, file_path)
    except Exception as e:
        logger.warning(f"File was not uploaded: {e}")
        raise HTTPException(status_code=400, detail=f"File was not uploaded: {e}")

    animal_files.append(file_url)
    animal.extra_photos_url = json.dumps(animal_files)

    await db.commit()
    await db.refresh(animal)

    return {"url": file_url}


@router.delete("/{animal_id}/files", status_code=204)
async def delete_animal_file(
    animal_id: int,
    url: AnimalFileUrl,
    current_user: User = Depends(require_admin),
    storage=Depends(get_storage_backend),
    db=Depends(get_db),
):
    animal = await get_animal_and_authorize_access(db, animal_id, current_user)

    import json

    animal_files = json.loads(animal.extra_photos_url) if animal.extra_photos_url else []

    if url.url not in animal_files:
        raise HTTPException(status_code=404, detail="Photo not found")

    try:
        await storage.delete_file(url.url)
    except Exception as e:
        logger.warning(f"File was not deleted: {e}")
        raise HTTPException(status_code=400, detail=f"File was not deleted: {e}")

    animal_files.remove(url.url)
    animal.extra_photos_url = json.dumps(animal_files) if animal_files else None

    await db.commit()

    return
