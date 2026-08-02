import shutil
import uuid
from pathlib import Path

from fastapi import UploadFile


class LocalStorageService:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def save_upload(self, upload: UploadFile) -> str:
        suffix = Path(upload.filename or "document.pdf").suffix.lower()
        key = f"{uuid.uuid4()}{suffix}"
        path = self.root / key
        with path.open("wb") as destination:
            shutil.copyfileobj(upload.file, destination)
        return key

    def path_for(self, key: str) -> Path:
        return self.root / key
