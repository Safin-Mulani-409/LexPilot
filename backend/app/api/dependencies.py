from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.database.session import get_db
from app.services.ai import AIService
from app.services.cases import CaseService
from app.services.documents import DocumentService
from app.services.storage import LocalStorageService


def get_case_service(db: Session = Depends(get_db), settings: Settings = Depends(get_settings)) -> CaseService:
    return CaseService(db, settings, LocalStorageService(settings.upload_dir), DocumentService(), AIService(settings))
