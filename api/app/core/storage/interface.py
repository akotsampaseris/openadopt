from abc import ABC, abstractmethod

from fastapi import UploadFile


class StorageBackend(ABC):
    """Abstract interface for file storage backends"""

    @abstractmethod
    async def upload_file(self, file: UploadFile, path: str) -> str:
        pass

    @abstractmethod
    async def delete_file(self, url: str) -> None:
        pass

    @abstractmethod
    async def file_exists(self, url: str) -> bool:
        pass
