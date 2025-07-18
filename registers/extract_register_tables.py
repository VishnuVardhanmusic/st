# module_registers/extract_register_tables.py

import pdfplumber
import json
from pathlib import Path

REGISTER_PDF_PATH = Path("data/UART_Register_Manual.pdf")
OUTPUT_JSON_PATH = Path("output/extracted_registers.json")

EXPECTED_HEADERS = ["bit", "field", "type", "reset", "description"]


def headers_match(headers: list) -> bool:
    """Check if table headers approximately match expected register field headers."""
    normalized = [h.strip().lower() for h in headers]
    return all(any(expected in h for h in normalized) for expected in EXPECTED_HEADERS)


def extract_register_tables(pdf_path: Path) -> list:
    """Extract register tables from the PDF where headers match register table pattern."""
    all_tables = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            try:
                tables = page.extract_tables()
                for table in tables:
                    if not table or len(table) < 2:
                        continue

                    headers = table[0]
                    if headers_match(headers):
                        rows = table[1:]  # skip header
                        structured_rows = [
                            dict(zip(headers, row)) for row in rows if row and len(row) == len(headers)
                        ]

                        all_tables.append({
                            "page": page_num,
                            "headers": headers,
                            "rows": structured_rows
                        })

            except Exception as e:
                print(f"Error processing page {page_num}: {e}")

    return all_tables


def save_register_data(tables: list, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(tables, f, indent=2, ensure_ascii=False)
    print(f"✅ Extracted register tables saved to {output_path}")


if __name__ == "__main__":
    tables = extract_register_tables(REGISTER_PDF_PATH)
    save_register_data(tables, OUTPUT_JSON_PATH)
