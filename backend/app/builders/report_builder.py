from app.schemas.report import (
    CaseAnalysis,
    LegalIssue,
    Party,
    SourcedItem,
    TimelineEvent,
)


class ReportBuilder:

    def build(
        self,
        *,
        summary: str,
        court_name: str | None,
        judge_name: str | None,
        case_number: str | None,
        case_year: str | None,
        case_type: str | None,
        parties: list[Party],
        legal_sections: list[str],
        legal_issues: list[LegalIssue],
        important_facts: list[SourcedItem],
        timeline: list[TimelineEvent],
        evidence: list[str],
        relief_sought: str | None,
        missing_information: list[str],
        suggested_questions: list[str],
        hearing_preparation_checklist: list[str],
        next_steps: list[str],
        confidence_score: int,
        disclaimer: str,
    ) -> CaseAnalysis:

        return CaseAnalysis(
            case_summary=summary,

            court_name=court_name,
            judge_name=judge_name,
            case_number=case_number,
            case_year=case_year,
            case_type=case_type,

            parties=parties,

            legal_sections=legal_sections,
            legal_issues=legal_issues,

            important_facts=important_facts,
            timeline=timeline,

            evidence=evidence,
            relief_sought=relief_sought,

            missing_information=missing_information,
            suggested_questions=suggested_questions,
            hearing_preparation_checklist=hearing_preparation_checklist,
            next_steps=next_steps,

            confidence_score=confidence_score,

            disclaimer=disclaimer,
        )