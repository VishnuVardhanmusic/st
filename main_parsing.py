# main.py

from pathlib import Path
from parser.extractor import extract_text_blocks_from_pdf
from parser.classifier import classify_text_blocks
from parser.utils import save_blocks_to_json, preview_blocks
from config.parser_config import EXTRACTION_OUTPUT_PATH

# Define input PDF directory and target filenames
PDF_DIR = Path("data")
PDF_FILES = [
    PDF_DIR / "UART_Introduction.pdf",
    PDF_DIR / "UART_TRM.pdf",
    PDF_DIR / "UART_Register_Manual.pdf"
]


def main():
    all_blocks = []

    print("📄 Starting PDF extraction and classification...\n")

    for pdf_file in PDF_FILES:
        print(f"🔍 Processing: {pdf_file.name}")
        extracted = extract_text_blocks_from_pdf(pdf_file)
        classified = classify_text_blocks(extracted)
        all_blocks.extend(classified)

    # Save to JSON
    output_path = Path(EXTRACTION_OUTPUT_PATH)
    save_blocks_to_json(all_blocks, output_path)

    # Preview first few blocks
    preview_blocks(all_blocks, n=10)

    print(f"\n✅ Parsing complete. Total blocks extracted: {len(all_blocks)}")
    print(f"📝 Output saved to: {output_path.resolve()}")


if __name__ == "__main__":
    main()
