# parser/extractor.py

import fitz  # PyMuPDF
from pathlib import Path
from typing import List, Dict
from config import parser_config as cfg


def extract_text_blocks_from_pdf(pdf_path: Path) -> List[Dict]:
    """
    Extracts all text spans from a given PDF using PyMuPDF and returns structured blocks.
    Each span includes font metadata and bounding box for layout analysis.
    """
    doc = fitz.open(pdf_path)
    blocks_all = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block["type"] != 0:
                continue  # Skip images or non-text blocks

            for line in block.get("lines", []):
                for span in line["spans"]:
                    text = span["text"].strip()
                    if len(text) < cfg.MIN_TEXT_LENGTH:
                        continue

                    block_info = {
                        "origin": pdf_path.name,
                        "page": page_num,
                        "text": text,
                        "font": span.get("font", ""),
                        "size": span.get("size", 0),
                        "flags": span.get("flags", 0),
                        "bbox": span.get("bbox", []),
                        "color": span.get("color", 0)
                    }
                    blocks_all.append(block_info)

    return blocks_all
