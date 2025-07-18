# module_full_codegen/build_final_prompt.py

import os
import json
from pathlib import Path

RESPONSES_DIR = Path("output/llm_responses")
REGISTER_TXT_PATH = RESPONSES_DIR / "06_register_level_pseudo.txt"


def load_json_pseudos():
    """Load all structured pseudo code JSON files (00–05)."""
    pseudo_sections = []

    for file in sorted(RESPONSES_DIR.glob("[0-5][0-9]_*.json")):
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
            pseudo_sections.append({
                "section_id": data["section_id"],
                "title": data["title"],
                "pseudo_code": data["pseudo_code"]
            })

    return pseudo_sections


def load_register_txt_as_json():
    """Wrap the register-level .txt into pseudo_code format."""
    with open(REGISTER_TXT_PATH, "r", encoding="utf-8") as f:
        content = f.read().strip()

    return {
        "section_id": 6,
        "title": "Register-Level Peripheral Behavior",
        "pseudo_code": content
    }


def build_final_prompt() -> str:
    """Build a single prompt string from 6 pseudo code blocks."""
    sections = load_json_pseudos()
    sections.append(load_register_txt_as_json())
    sections.sort(key=lambda x: x["section_id"])

    prompt_sections = "\n\n".join([
        f"### Section {s['section_id']:02d}: {s['title']}\n{s['pseudo_code']}" for s in sections
    ])

    final_prompt = f"""\
You are a senior embedded software engineer working on the MSPM0 microcontroller.
Using the combined pseudocode blocks below, generate the complete embedded C code
for the UART peripheral, including initialization, data transmission/reception,
interrupt handling, and proper usage of all device-specific registers.

Constraints:
- Follow MSPM0 register usage exactly (from section 06)
- Use peripheral-safe coding practices
- Separate header and source code if needed
- Add comments to guide understanding
- DO NOT hallucinate values or registers

{prompt_sections}

### Output:
- Provide full UART driver implementation code
- Separate .h and .c code blocks using clear boundaries
- Include preprocessor guards, typedefs, init APIs, etc.
"""
    return final_prompt.strip()
