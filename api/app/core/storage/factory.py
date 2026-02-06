from app.core.config import settings
from app.core.storage.interface import StorageBackend
from app.core.storage.local import LocalStorage


def get_storage_backend() -> StorageBackend:
    """
    Factory function to get the configured storage backend.

    Returns:
        StorageBackend instance based on STORAGE_BACKEND
    """
    if settings.STORAGE_BACKEND == "local":
        return LocalStorage()
    else:
        raise ValueError(f"Uknown storage backend: {settings.STORAGE_BACKEND}")
