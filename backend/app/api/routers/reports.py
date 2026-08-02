from fastapi import APIRouter, Depends

from app.api.dependencies import get_case_service
from app.schemas.case import ReportResponse
from app.services.cases import CaseService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(report_id: str, service: CaseService = Depends(get_case_service)) -> ReportResponse:
    return service.get_report(report_id)
