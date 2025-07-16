import pdfplumber
import os
import re
import logging
from pathlib import Path

# ────────────────
# Logger setup
# ────────────────
logging.basicConfig(level=logging.INFO, format="🔍 [%(levelname)s] %(message)s")


def extract_section(text, start_keywords, end_keywords):
    """
    Extract section text between start and end keywords (case-insensitive).
    """
    pattern = re.compile(
        rf"({'|'.join(start_keywords)})(.*?)(?=({'|'.join(end_keywords)}|$))",
        re.IGNORECASE | re.DOTALL
    )
    match = pattern.search(text)
    if match:
        return match.group(0).strip()
    return None


def parse_trm(file_path):
    """
    Extract 'Overview' and 'Operations' sections from a TRM PDF file.
    Returns a dictionary with keys: 'overview', 'operations'
    """
    if not Path(file_path).exists():
        logging.error(f"File not found: {file_path}")
        return {"overview": "", "operations": ""}

    logging.info(f"Opening TRM PDF: {file_path}")
    full_text = ""

    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += "\n" + text

    except Exception as e:
        logging.error(f"Failed to open PDF: {e}")
        return {"overview": "", "operations": ""}

    # Normalize white spaces
    full_text = re.sub(r"[ \t]+", " ", full_text)

    # Extract sections
    logging.info("Extracting 'Overview' section...")
    overview = extract_section(
        full_text,
        start_keywords=["Overview"],
        end_keywords=["Functional Description", "Features", "Operation", "Initialization"]
    )

    logging.info("Extracting 'Operations' section...")
    operations = extract_section(
        full_text,
        start_keywords=["Operation", "Operations", "Functionality", "Working"],
        end_keywords=["Configuration", "Register", "Usage", "Initialization", "Example"]
    )

    if not overview:
        logging.warning("No 'Overview' section found.")
    if not operations:
        logging.warning("No 'Operations' section found.")

    return {
        "overview": overview or "",
        "operations": operations or ""
    }


# ────────────────
# CLI Testing (Optional)
# ────────────────
if __name__ == "__main__":
    path = "data/specs/part_a_trm.pdf"
    result = parse_trm(path)

    print("\n\n🧠 OVERVIEW SECTION:")
    print(result["overview"][:1000])  # print first 1000 characters

    print("\n\n⚙️ OPERATIONS SECTION:")
    print(result["operations"][:1000])  # print first 1000 characters
