import pdfplumber
import pandas as pd
import logging
import re
from pathlib import Path

# ────────────────
# Logger setup
# ────────────────
logging.basicConfig(level=logging.INFO, format="📦 [%(levelname)s] %(message)s")


def clean_register_name(name):
    return re.sub(r'\s+', '', name.strip().upper())


def parse_register_pdf(file_path):
    """
    Parse register manual PDF and extract structured register data.
    Returns a dict with register names as keys.
    """
    if not Path(file_path).exists():
        logging.error(f"File not found: {file_path}")
        return {}

    logging.info(f"Parsing Register Manual PDF: {file_path}")
    register_data = {}

    try:
        with pdfplumber.open(file_path) as pdf:
            for page_number, page in enumerate(pdf.pages):
                tables = page.extract_tables()
                if not tables:
                    continue

                for table in tables:
                    # Expecting 5 columns (name, addr, access, reset, desc)
                    if len(table[0]) < 5:
                        continue  # skip malformed tables

                    for row in table[1:]:  # skip header
                        try:
                            name, addr, access, reset, desc = row[:5]
                            reg_name = clean_register_name(name)
                            register_data[reg_name] = {
                                "address": addr.strip(),
                                "access": access.strip(),
                                "reset": reset.strip(),
                                "description": desc.strip()
                            }
                        except Exception as e:
                            logging.warning(f"Skipping malformed row on page {page_number+1}: {row} — {e}")
                            continue

    except Exception as e:
        logging.error(f"Failed to parse register PDF: {e}")
        return {}

    logging.info(f"Total registers parsed: {len(register_data)}")
    return register_data


# ────────────────
# CLI Testing (Optional)
# ────────────────
if __name__ == "__main__":
    path = "data/specs/part_b_registers.pdf"
    reg_map = parse_register_pdf(path)

    # Preview a few
    for k, v in list(reg_map.items())[:3]:
        print(f"\n🔧 {k} → {v}")
