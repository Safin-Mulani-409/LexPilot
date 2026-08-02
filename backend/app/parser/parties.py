import re


ROLE_PATTERNS = {
    "Plaintiff": [
        r"plaintiff\s*[:\-]\s*(.+)",
        r"petitioner\s*[:\-]\s*(.+)",
        r"complainant\s*[:\-]\s*(.+)",
        r"applicant\s*[:\-]\s*(.+)",
    ],
    "Defendant": [
        r"defendant\s*[:\-]\s*(.+)",
        r"respondent\s*[:\-]\s*(.+)",
        r"accused\s*[:\-]\s*(.+)",
        r"opponent\s*[:\-]\s*(.+)",
    ],
}


def extract_parties(text: str) -> list[dict]:
    """
    Extract parties from common Indian court document formats.
    Returns:
    [
        {"name": "...", "role": "..."}
    ]
    """

    parties = []
    seen = set()

    clean = re.sub(r"\s+", " ", text)

    # --------------------------------------------------
    # Pattern 1
    # A vs B
    # --------------------------------------------------

    versus = re.search(
        r"([A-Z][A-Za-z .,&()'-]{3,120})\s+(?:v\.?|vs\.?|versus)\s+([A-Z][A-Za-z .,&()'-]{3,120})",
        clean,
        re.IGNORECASE,
    )

    if versus:

        p1 = versus.group(1).strip()
        p2 = versus.group(2).strip()

        parties.append(
            {
                "name": p1,
                "role": "Plaintiff / Petitioner",
            }
        )

        parties.append(
            {
                "name": p2,
                "role": "Defendant / Respondent",
            }
        )

        seen.add(p1.lower())
        seen.add(p2.lower())

    # --------------------------------------------------
    # Pattern 2
    # Plaintiff:
    # Defendant:
    # etc.
    # --------------------------------------------------

    for role, patterns in ROLE_PATTERNS.items():

        for pattern in patterns:

            matches = re.findall(pattern, clean, re.IGNORECASE)

            for match in matches:

                name = match.strip()

                name = re.sub(r"\s{2,}", " ", name)

                if (
                    len(name) > 2
                    and name.lower() not in seen
                ):

                    parties.append(
                        {
                            "name": name,
                            "role": role,
                        }
                    )

                    seen.add(name.lower())

    return parties