import re


SECTION_PATTERNS = [

    # IPC
    r"Section\s+\d+[A-Za-z\-]*\s+IPC",
    r"Sec\.?\s+\d+[A-Za-z\-]*\s+IPC",

    # CrPC
    r"Section\s+\d+[A-Za-z\-]*\s+CrPC",
    r"Sec\.?\s+\d+[A-Za-z\-]*\s+CrPC",

    # CPC
    r"Order\s+[IVXLC0-9]+\s+Rule\s+\d+[A-Za-z\-]*",
    r"Order\s+[IVXLC0-9]+\s+Rule\s+\d+[A-Za-z\-]*\s+CPC",

    # Constitution
    r"Article\s+\d+[A-Za-z\-]*",

    # Negotiable Instruments Act
    r"Section\s+\d+\s+NI\s+Act",
    r"Section\s+\d+\s+Negotiable\s+Instruments\s+Act",

    # Arbitration
    r"Section\s+\d+\s+Arbitration\s+Act",

    # Hindu Marriage Act
    r"Section\s+\d+\s+Hindu\s+Marriage\s+Act",

    # Companies Act
    r"Section\s+\d+\s+Companies\s+Act",

    # Consumer Protection
    r"Section\s+\d+\s+Consumer\s+Protection\s+Act",

    # Information Technology Act
    r"Section\s+\d+\s+IT\s+Act",
    r"Section\s+\d+\s+Information\s+Technology\s+Act",
]


def extract_legal_sections(text: str) -> list[str]:
    """
    Extract legal sections referenced in the document.
    """

    found = set()

    clean = re.sub(r"\s+", " ", text)

    for pattern in SECTION_PATTERNS:

        matches = re.findall(pattern, clean, re.IGNORECASE)

        for match in matches:

            found.add(match.strip())

    return sorted(found)