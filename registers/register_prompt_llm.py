# module_registers/register_prompt_llm.py

import json
from pathlib import Path
from litellm import completion
from config.llm_config import MODEL_NAME, API_KEY, BASE_URL

INPUT_JSON = Path("output/extracted_registers.json")
OUTPUT_TXT = Path("output/llm_responses/06_register_level_pseudo.txt")


def load_register_data(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def format_table_for_prompt(table_obj: dict) -> str:
    page = table_obj["page"]
    rows = table_obj["rows"]

    formatted_rows = "\n".join([
        f"- Bit {r.get('Bit', '')}: `{r.get('Field', '')}` ({r.get('Type', '')}, Reset={r.get('Reset', '')}) — {r.get('Description', '')}"
        for r in rows
    ])

    return f"### Register Fields (Page {page}):\n{formatted_rows}\n"


def build_register_prompt(register_tables: list) -> str:
    context_blocks = [format_table_for_prompt(tbl) for tbl in register_tables]

    return f"""\
You are an embedded systems expert specializing in low-level driver development.

Below are the register field descriptions extracted from the UART Register Manual of the MSPM0 device. 
Your task is to write a detailed pseudo code that:
- Initializes UART peripheral step-by-step
- Properly uses all relevant registers
- Follows correct bit configurations (e.g., write only when allowed, preserve reserved fields)
- Honors reset values and constraints
- Covers data transfer, interrupt config, and power-saving logic if found

{''.join(context_blocks)}

### Output Format:
- Use structured pseudocode blocks
- Include register names and bit operations
- Add brief comments to explain steps
""".strip()


def call_llm(prompt: str) -> str:
    try:
        response = completion(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            api_key=API_KEY,
            base_url=BASE_URL,
            temperature=0.2,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"❌ LLM error: {e}")
        return "[ERROR] LLM failed to respond."


def save_response(text: str, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"✅ Register-level pseudo code saved to {path}")


if __name__ == "__main__":
    data = load_register_data(INPUT_JSON)
    prompt = build_register_prompt(data)
    response = call_llm(prompt)
    save_response(response, OUTPUT_TXT)
