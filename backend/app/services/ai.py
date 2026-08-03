import json
import re

from openai import OpenAI

from app.builders.report_builder import ReportBuilder
from app.core.config import Settings
from app.parser.court import extract_court_details
from app.parser.parties import extract_parties
from app.parser.sections import extract_legal_sections
from app.prompts.case_analysis import CASE_ANALYSIS_INSTRUCTIONS
from app.schemas.report import (
    CaseAnalysis,
    LegalIssue,
    Party,
    SourcedItem,
    TimelineEvent,
)


class AIService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.report_builder = ReportBuilder()

    def analyze_case(self, text: str) -> CaseAnalysis:
        """
        Main entry point.
        If OpenAI is unavailable for ANY reason,
        automatically fall back to offline analysis.
        """

        if not self.settings.openai_api_key:
            return self._offline_analysis(
            text,
            "AI analysis unavailable in this deployment."
        )

        client = OpenAI(api_key=self.settings.openai_api_key)

        schema = CaseAnalysis.model_json_schema()

        try:

            print("=" * 80)
            print("GENERATED JSON SCHEMA")
            print("=" * 80)
            print(json.dumps(schema, indent=2))

            with open("schema.json", "w", encoding="utf-8") as f:
                json.dump(schema, f, indent=2)

            response = client.responses.create(
                model=self.settings.openai_model,
                instructions=CASE_ANALYSIS_INSTRUCTIONS,
                input=f"Case document:\n{text[:120000]}",
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "case_analysis",
                        "strict": True,
                        "schema": schema,
                    }
                },
            )

            return CaseAnalysis.model_validate_json(response.output_text)

        except Exception as e:

            print("=" * 80)
            print("OPENAI FAILED")
            print(e)
            print("=" * 80)

            return self._offline_analysis(text, str(e))
            

    def _offline_analysis(self, text: str, reason: str) -> CaseAnalysis:
        """Deterministic fallback analysis used when OpenAI is unavailable."""

        # ---------------------------------------------------------
        # Split document into pages
        # ---------------------------------------------------------
        page_blocks = re.split(r"(?=\[Page \d+\])", text)

        facts: list[SourcedItem] = []
        timeline: list[TimelineEvent] = []

        date_pattern = re.compile(r"\b\d{1,2}[./-]\d{1,2}[./-]\d{2,4}\b")

        # ---------------------------------------------------------
        # Extract Facts & Timeline
        # ---------------------------------------------------------
        for block in page_blocks:
            page_match = re.match(r"\[Page (\d+)\]", block)
            page_number = int(page_match.group(1)) if page_match else 1
            clean = re.sub(r"\[Page \d+\]", "", block).strip()

            sentences = [
                s.strip()
                for s in re.split(r"(?<=[.!?।])\s+", clean)
                if len(s.strip()) > 35
            ]

            for sentence in sentences[:2]:
                if len(facts) < 6:
                    facts.append(
                        SourcedItem(
                            text=sentence[:420],
                            page_references=[page_number],
                        )
                    )

                for value in date_pattern.findall(sentence):
                    if len(timeline) < 6:
                        timeline.append(
                            TimelineEvent(
                                date=value,
                                event=sentence[:260],
                                page_references=[page_number],
                            )
                        )

        # ---------------------------------------------------------
        # Plain Text
        # ---------------------------------------------------------
        plain_text = re.sub(r"\[Page \d+\]", "", text)

        # ---------------------------------------------------------
        # Court
        # ---------------------------------------------------------
        court = extract_court_details(plain_text)

        court_name = court.get("court_name")
        judge_name = court.get("judge_name")
        case_number = court.get("case_number")
        case_year = court.get("case_year")
        case_type = None

        # ---------------------------------------------------------
        # Parties
        # ---------------------------------------------------------
        parsed_parties = extract_parties(plain_text)

        parties = [
            Party(
                name=item["name"],
                role=item["role"],
            )
            for item in parsed_parties
        ]

        # ---------------------------------------------------------
        # Sections
        # ---------------------------------------------------------
        legal_sections = extract_legal_sections(plain_text)

        # ---------------------------------------------------------
        # Legal Issues
        # ---------------------------------------------------------
        issues: list[LegalIssue] = []

        issue_rules = [
            (
                r"counterclaim",
                "Counterclaim / procedural permission",
            ),
            (
                r"order\s+viii|rule\s+9",
                "Civil procedure compliance",
            ),
            (
                r"bail",
                "Bail and custody",
            ),
            (
                r"divorce|marriage",
                "Matrimonial relief",
            ),
            (
                r"contract|agreement",
                "Contractual obligations",
            ),
        ]

        lower_text = plain_text.lower()

        for pattern, label in issue_rules:
            if re.search(pattern, lower_text):
                issues.append(
                    LegalIssue(
                        issue=label,
                        context="Detected from document content.",
                    )
                )

        # ---------------------------------------------------------
        # Summary
        # ---------------------------------------------------------
        if facts:
            summary = facts[0].text
        else:
            summary = (
                "The document was processed locally "
                "but extractable information was limited."
            )

        # ---------------------------------------------------------
        # Confidence
        # ---------------------------------------------------------
        confidence = 0

        if court_name:
            confidence += 20
        if parties:
            confidence += 20
        if legal_sections:
            confidence += 20
        if facts:
            confidence += 20
        if timeline:
            confidence += 20

        # ---------------------------------------------------------
        # Build Report
        # ---------------------------------------------------------
        return self.report_builder.build(
            summary="The uploaded legal document was successfully processed locally. A structured legal report has been generated from the extracted text.",
            court_name=court_name,
            judge_name=judge_name,
            case_number=case_number,
            case_year=case_year,
            case_type=case_type,
            parties=parties,
            legal_sections=legal_sections,
            legal_issues=issues,
            important_facts=facts,
            timeline=timeline,
            evidence=[],
            relief_sought=None,
            missing_information=[
                "Advanced AI analysis unavailable. Using preliminary analysis mode.",
                "Verify extracted facts against the original PDF.",
            ],
            suggested_questions=[
                "What precise relief is sought?",
                "Which originals support each material fact?",
                "What is the next hearing date?",
            ],
            hearing_preparation_checklist=[
                "Verify extracted facts.",
                "Carry original documents.",
                "Review relief sought.",
            ],
            next_steps=[
                "Configure OpenAI credits.",
                "Review the extracted report.",
            ],
            confidence_score=confidence,
            disclaimer=(
                "Offline analysis only. "
                "This is not legal advice."
            ),
        )


    def _demo_analysis(self, text: str) -> CaseAnalysis:
        """
        Demo mode used when OPENAI_API_KEY is not configured.
        """
        preview = " ".join(
            text.replace("[Page 1]", "").split()
        )[:400]

        return self.report_builder.build(
            summary=(
                f"Demo analysis. "
                f"Document contains {len(text):,} extracted characters. "
                f"Preview: {preview}"
            ),
            court_name=None,
            judge_name=None,
            case_number=None,
            case_year=None,
            case_type=None,
            parties=[],
            legal_sections=[],
            legal_issues=[],
            important_facts=[],
            timeline=[],
            evidence=[],
            relief_sought=None,
            missing_information=[
                "Review extracted facts.",
                "Verify parties and legal sections.",
                "Prepare hearing notes.",
            ],
            suggested_questions=[
                "What relief is sought?",
                "Who are the parties?",
            ],
            hearing_preparation_checklist=[
                "Verify document contents."
            ],
            next_steps=[
                "Configure OpenAI API Key."
            ],
            confidence_score=0,
            disclaimer=(
                "Demo mode only. "
                "Not legal advice."
            ),
        )