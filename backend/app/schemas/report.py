from pydantic import BaseModel, ConfigDict, Field


class StrictResponseModel(BaseModel):
    """
    Base model for OpenAI Structured Outputs.
    Every object forbids additional properties.
    """

    model_config = ConfigDict(extra="forbid")


# ----------------------------------------------------------------------
# Basic Models
# ----------------------------------------------------------------------


class Party(StrictResponseModel):
    name: str
    role: str


class SourcedItem(StrictResponseModel):
    text: str
    page_references: list[int]


class TimelineEvent(StrictResponseModel):
    date: str | None
    event: str
    page_references: list[int]


class LegalIssue(StrictResponseModel):
    issue: str
    context: str


# ----------------------------------------------------------------------
# Main Report
# ----------------------------------------------------------------------


class CaseAnalysis(StrictResponseModel):
    # ------------------------------------------------------------------
    # Executive Summary
    # ------------------------------------------------------------------

    case_summary: str

    # ------------------------------------------------------------------
    # Court Information
    # ------------------------------------------------------------------

    court_name: str | None
    judge_name: str | None
    case_number: str | None
    case_year: str | None
    case_type: str | None

    # ------------------------------------------------------------------
    # Parties
    # ------------------------------------------------------------------

    parties: list[Party]

    # ------------------------------------------------------------------
    # Legal Analysis
    # ------------------------------------------------------------------

    legal_sections: list[str]

    legal_issues: list[LegalIssue]

    # ------------------------------------------------------------------
    # Facts
    # ------------------------------------------------------------------

    important_facts: list[SourcedItem]

    timeline: list[TimelineEvent]

    # ------------------------------------------------------------------
    # Evidence
    # ------------------------------------------------------------------

    evidence: list[str]

    relief_sought: str | None

    # ------------------------------------------------------------------
    # Review
    # ------------------------------------------------------------------

    missing_information: list[str]

    suggested_questions: list[str]

    hearing_preparation_checklist: list[str]

    next_steps: list[str]

    # ------------------------------------------------------------------
    # Confidence
    # ------------------------------------------------------------------

    confidence_score: int = Field(ge=0, le=100)

    # ------------------------------------------------------------------
    # Disclaimer
    # ------------------------------------------------------------------

    disclaimer: str