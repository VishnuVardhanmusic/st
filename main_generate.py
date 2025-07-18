# main_generate.py

import json
from pathlib import Path
from llm.prompt_builder import build_prompt
from llm.llm_client import call_llm
from llm.code_writer import save_pseudo_output  # Use save_code_output for C code too

STRUCTURED_SECTIONS_PATH = Path("output/structured_sections.json")


def load_sections(filepath: Path):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def main(task_type: str = "pseudo", section_limit: int = None):
    print(f"🚀 Starting LLM generation: task = {task_type}")
    sections = load_sections(STRUCTURED_SECTIONS_PATH)

    if section_limit:
        sections = sections[:section_limit]

    for idx, section in enumerate(sections):
        print(f"\n🔹 Processing Section {idx+1}/{len(sections)}: {section['title'][:60]}")

        prompt = build_prompt(section, task_type=task_type)
        response = call_llm(prompt)

        if task_type == "pseudo":
            save_pseudo_output(idx, section["title"], response)
        elif task_type == "code":
            from llm.code_writer import save_code_output
            save_code_output(idx, section["title"], response)
        else:
            print("❌ Unknown task type. Skipping.")

    print(f"\n✅ All sections processed. Outputs saved in: output/llm_responses/")


if __name__ == "__main__":
    # Can change task_type to "code" if full C code is desired
    main(task_type="pseudo", section_limit=5)
