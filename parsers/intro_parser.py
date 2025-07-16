import pdfplumber
import logging
from pathlib import Path
import re

# ────────────────
# Logger setup
# ────────────────
logging.basicConfig(level=logging.INFO, format="🧾 [%(levelname)s] %(message)s")


def parse_intro_pdf(file_path):
    """
    Extract full clean text from a general PDF (Part C).
    Assumes PDF contains point-wise guidelines, not structured headings.
    """
    if not Path(file_path).exists():
        logging.error(f"File not found: {file_path}")
        return ""

    logging.info(f"Parsing General Intro PDF (Part C): {file_path}")
    full_text = ""

    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    # Remove page numbers, headers if found
                    text = re.sub(r"Page \d+ of \d+", "", text)
                    text = re.sub(r"\n\s*\n", "\n", text)
                    full_text += text.strip() + "\n\n"
    except Exception as e:
        logging.error(f"Failed to read PDF: {e}")
        return ""

    logging.info("Intro text extraction completed.")
    return full_text.strip()


# ────────────────
# CLI Testing (Optional)
# ────────────────
if __name__ == "__main__":
    path = "data/specs/part_c_intro.pdf"
    content = parse_intro_pdf(path)

    print("\n📘 PART C — General Instructions (Preview):\n")
    print(content[:1000])  # Print first 1000 characters
