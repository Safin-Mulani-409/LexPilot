import re


def extract_court_details(text: str) -> dict:
    """
    Extract basic court metadata from Indian legal documents.
    """

    clean = re.sub(r"\s+", " ", text)

    court_name = None
    judge_name = None
    case_number = None
    case_year = None

    # Court name
    court_match = re.search(
        r"(IN THE .*?COURT.*?)(?=,|\.|\n)",
        text,
        re.IGNORECASE,
    )

    if court_match:
        court_name = court_match.group(1).strip()

    # Case number
    case_match = re.search(
        r"(\d+\/\d{4})",
        clean
    )

    if case_match:
        case_number = case_match.group(1)

        if "/" in case_number:
            case_year = case_number.split("/")[-1]

    # Judge
    judge_match = re.search(
        r"(HON'?BLE.*?JUSTICE\s+[A-Z .]+)",
        clean,
        re.IGNORECASE,
    )

    if judge_match:
        judge_name = judge_match.group(1).strip()

    return {
        "court_name": court_name,
        "judge_name": judge_name,
        "case_number": case_number,
        "case_year": case_year,
    }