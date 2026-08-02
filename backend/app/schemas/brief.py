from pydantic import BaseModel


class AdvocateBrief(BaseModel):
    case_title: str
    court: str | None = None
    judge: str | None = None

    summary: str

    key_issues: list[str]

    key_facts: list[str]

    documents_required: list[str]

    client_questions: list[str]

    hearing_strategy: list[str]

    risks: list[str]

    confidence: int