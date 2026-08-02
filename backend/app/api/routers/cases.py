from fastapi import APIRouter, Depends, File, Form, UploadFile, status

from app.api.dependencies import get_case_service
from app.schemas.case import AnalysisStartResponse, CaseListItem, CaseResponse
from app.services.cases import CaseService

router = APIRouter(prefix="/cases", tags=["cases"])


@router.get("", response_model=list[CaseListItem])
def list_cases(service: CaseService = Depends(get_case_service)) -> list[CaseListItem]:
    return service.list_cases()


@router.post("/upload", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
def upload_case(file: UploadFile = File(...), title: str | None = Form(default=None), service: CaseService = Depends(get_case_service)) -> CaseResponse:
    return service.upload(file, title)


@router.post("/{case_id}/analyze", response_model=AnalysisStartResponse, status_code=status.HTTP_202_ACCEPTED)
def analyze_case(case_id: str, service: CaseService = Depends(get_case_service)) -> AnalysisStartResponse:
    return service.start_analysis(case_id)


@router.get("/{case_id}", response_model=CaseResponse)
def get_case(case_id: str, service: CaseService = Depends(get_case_service)) -> CaseResponse:
    return service.get_case(case_id)
