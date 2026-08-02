from datetime import datetime, timezone

from fastapi import HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.config import Settings
from app.models.case import AnalysisReport, Case, CaseStatus, Document
from app.prompts.case_analysis import CASE_ANALYSIS_PROMPT_VERSION
from app.schemas.case import AnalysisStartResponse, CaseResponse, ReportResponse
from app.schemas.report import CaseAnalysis
from app.services.ai import AIService
from app.services.documents import DocumentExtractionError, DocumentService
from app.services.storage import LocalStorageService
import traceback


class CaseService:
    def __init__(self, db: Session, settings: Settings, storage: LocalStorageService, documents: DocumentService, ai: AIService) -> None:
        self.db, self.settings, self.storage, self.documents, self.ai = db, settings, storage, documents, ai

    def list_cases(self) -> list[CaseResponse]:
        cases = self.db.scalars(
            select(Case)
            .options(selectinload(Case.document), selectinload(Case.reports))
            .order_by(Case.created_at.desc())
        ).all()
        return [self._case_response(case) for case in cases]

    def upload(self, upload: UploadFile, title: str | None) -> CaseResponse:
        if not upload.filename or not upload.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only PDF case files are supported in this MVP.")
        key = self.storage.save_upload(upload)
        try:
            extracted_text, page_count = self.documents.extract_pdf(self.storage.path_for(key))
        except DocumentExtractionError as error:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error
        case = Case(title=title or upload.filename.rsplit(".", 1)[0], original_filename=upload.filename, storage_key=key)
        case.document = Document(page_count=page_count, extracted_text=extracted_text)
        self.db.add(case)
        self.db.commit()
        self.db.refresh(case)
        return self._case_response(case)

    def get_case(self, case_id: str) -> CaseResponse:
        case = self.db.scalar(select(Case).where(Case.id == case_id).options(selectinload(Case.document), selectinload(Case.reports)))
        if not case:
            raise HTTPException(status_code=404, detail="Case not found.")
        return self._case_response(case)

    def start_analysis(self, case_id: str) -> AnalysisStartResponse:
        case = self.db.scalar(
            select(Case)
            .where(Case.id == case_id)
            .options(selectinload(Case.document))
        )

        if not case or not case.document:
            raise HTTPException(status_code=404, detail="Case not found.")

        report = AnalysisReport(
            case_id=case.id,
            status=CaseStatus.processing,
            model=self.settings.openai_model,
            prompt_version=CASE_ANALYSIS_PROMPT_VERSION,
        )

        case.status = CaseStatus.processing
        self.db.add(report)
        self.db.commit()

        print("STEP 1 - Report created")

        try:
            print("STEP 2 - Calling AI")

            analysis = self.ai.analyze_case(case.document.extracted_text)

            print("STEP 3 - AI returned")

            report.analysis_json = analysis.model_dump()

            report.status = CaseStatus.ready
            case.status = CaseStatus.ready
            report.completed_at = datetime.now(timezone.utc)

            print("STEP 4 - Saving report")

        except Exception as error:
            import traceback

            traceback.print_exc()

            print("=" * 80)
            print("ANALYSIS FAILED")
            print(error)
            print("=" * 80)

            report.status = CaseStatus.failed
            case.status = CaseStatus.failed
            report.error_message = str(error)

        # THIS WAS MISSING
        self.db.commit()

        print("STEP 5 - Database committed")

        return AnalysisStartResponse(
            case_id=case.id,
            report_id=report.id,
            status=report.status,
        )

    def get_report(self, report_id: str) -> ReportResponse:
        report = self.db.get(AnalysisReport, report_id)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found.")
        return self._report_response(report)

    def _case_response(self, case: Case) -> CaseResponse:
        report = max(case.reports, key=lambda item: item.created_at) if case.reports else None
        return CaseResponse(id=case.id, title=case.title, original_filename=case.original_filename, status=case.status, created_at=case.created_at, page_count=case.document.page_count if case.document else None, latest_report=self._report_response(report) if report else None)

    @staticmethod
    def _report_response(report: AnalysisReport) -> ReportResponse:
        return ReportResponse(id=report.id, case_id=report.case_id, status=report.status, analysis=CaseAnalysis.model_validate(report.analysis_json) if report.analysis_json else None, error_message=report.error_message, created_at=report.created_at, completed_at=report.completed_at)
