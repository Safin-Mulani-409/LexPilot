from datetime import datetime

from pydantic import BaseModel

from app.models.case import CaseStatus
from app.schemas.report import CaseAnalysis


class CaseListItem(BaseModel):
    id: str
    title: str
    original_filename: str
    status: CaseStatus
    created_at: datetime

    model_config = {"from_attributes": True}


class ReportResponse(BaseModel):
    id: str
    case_id: str
    status: CaseStatus
    analysis: CaseAnalysis | None = None
    error_message: str | None = None
    created_at: datetime
    completed_at: datetime | None = None


class CaseResponse(CaseListItem):
    page_count: int | None = None
    latest_report: ReportResponse | None = None


class AnalysisStartResponse(BaseModel):
    case_id: str
    report_id: str
    status: CaseStatus
