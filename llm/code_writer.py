# module3/code_writer.py

import os
import json
from pathlib import Path
from typing import Dict

OUTPUT_DIR = Path("output/llm_responses")


def save_pseudo_output(section_id: int, section_title: str, response: str):
    """
    Save pseudo code response in both JSON (for future LLM) and TXT (for human viewing).
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    safe_title = _sanitize_filename(section_title)

    json_path = OUTPUT_DIR / f"{section_id:02d}_{safe_title}_pseudo.json"
    txt_path = OUTPUT_DIR / f"{section_id:02d}_{safe_title}_pseudo.txt"

    # Save structured JSON
    json_data = {
        "section_id": section_id,
        "title": section_title,
        "task": "pseudo",
        "pseudo_code": response.strip()
    }
    with open(json_path, "w", encoding="utf-8") as f_json:
        json.dump(json_data, f_json, indent=2, ensure_ascii=False)

    # Save plain readable .txt
    with open(txt_path, "w", encoding="utf-8") as f_txt:
        f_txt.write(f"### Pseudo Code for Section: {section_title}\n\n")
        f_txt.write(response.strip())

    print(f"✅ Pseudo code saved: {json_path.name}, {txt_path.name}")


def save_code_output(section_id: int, section_title: str, response: str):
    """
    Save generated C code into .c or .h file depending on structure.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    safe_title = _sanitize_filename(section_title)

    # Detect whether to use .c or .h (simple heuristic)
    ext = ".h" if "#define" in response or "extern" in response else ".c"
    code_path = OUTPUT_DIR / f"{section_id:02d}_{safe_title}_generated{ext}"

    with open(code_path, "w", encoding="utf-8") as f_code:
        f_code.write(response.strip())

    print(f"✅ C code saved: {code_path.name}")


def _sanitize_filename(title: str) -> str:
    """
    Make a safe filename from a title (remove spaces, symbols).
    """
    return title.strip().lower().replace(" ", "_").replace("/", "_")[:40]
