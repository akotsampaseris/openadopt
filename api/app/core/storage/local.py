import logging
from pathlib import Path

import aiofiles
import shutil
from fastapi import UploadFile

from app.core.config import settings
from app.core.storage.interface import StorageBackend

logger = logging.getLogger(__name__)


class LocalStorage(StorageBackend):
    """Local storage backend"""

    def __init__(self):
        self.base_path = Path(settings.STORAGE_LOCAL_PATH)
        self.base_url = settings.STORAGE_LOCAL_URL

        # Create uploads dir if it doesn't exist
        self.base_path.mkdir(parents=True, exist_ok=True)

    async def upload_file(self, file: UploadFile, path: str) -> str:
        file_path = Path(self.base_path / path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Uploading file {file.filename} to {file_path}")
        async with aiofiles.open(file_path, "wb") as f:
            content = await file.read()
            await f.write(content)

        logger.info(f"File {file.filename} uploaded successfully")
        return f"{self.base_url}/{path}"

    async def delete_file(self, url: str) -> None:
        path = url.replace(self.base_url + "/", "")
        file_path = Path(self.base_path / path)

        if not file_path.exists():
            logger.warning(f"File at {url} does not exist")
            raise Exception(f"File at {url} does not exist")

        file_path.unlink()
        logger.info(f"File at {url} deleted successfully")
        return

    async def delete_dir(self, url: str) -> None:
        path = url.replace(self.base_url + "/", "")
        dir_path = Path(self.base_path / path)

        if dir_path.exists():
            shutil.rmtree(dir_path)

        return

    async def file_exists(self, url: str) -> bool:
        path = url.replace(self.base_url + "/", "")
        file_path = self.base_path / path
        return file_path.exists()
