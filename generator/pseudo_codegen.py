import os
import logging
from pathlib import Path

from parsers.trm_parser import parse_trm
from parsers.register_parser import parse_register_pdf
from parsers.intro_parser import parse_intro_pdf
from prompt_engine.build_pseudo_prompt import build_pseudo_prompt
from llm_engine.call_llm import call_llm
from llm_engine.extract_code import extract_c_code_block

# ────────────────
# Logger setup
# ────────────────
logging.basicConfig(level=logging.INFO, format="🛠️ [%(levelname)s] %(message)s")


def generate_pseudocode(
    peripheral_name: str,
    device_family: str,
    trm_path: str,
    register_path: str,
    intro_path: str
):
    """
    Main function to run Part A+B+C through LLM and save pseudocode output.
    """
    logging.info("🚀 Starting pseudocode generation pipeline...")

    # 1. Parse all 3 PDFs
    logging.info("📖 Parsing Part A (TRM)...")
    trm_data = parse_trm(trm_path)

    logging.info("📖 Parsing Part B (Registers)...")
    register_data = parse_register_pdf(register_path)

    logging.info("📖 Parsing Part C (Intro)...")
    intro_text = parse_intro_pdf(intro_path)

    # 2. Build prompt
    prompt = build_pseudo_prompt(
        peripheral_name=peripheral_name,
        device_family=device_family,
        overview_text=trm_data.get("overview", ""),
        operations_text=trm_data.get("operations", ""),
        register_map=register_data,
        intro_text=intro_text
    )

    # 3. Call LLM
    llm_response = call_llm(prompt)

    # 4. Extract code
    pseudocode = extract_c_code_block(llm_response)

    # 5. Save output
    output_dir = Path("outputs/pseudocode")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{peripheral_name.lower()}_pseudo.c"
    with open(output_file, "w") as f:
        f.write(pseudocode)

    logging.info(f"✅ Pseudocode saved to {output_file}")


# ────────────────
# CLI Trigger
# ────────────────
if __name__ == "__main__":
    generate_pseudocode(
        peripheral_name="UART0",
        device_family="MSPM0G3507",
        trm_path="data/specs/part_a_trm.pdf",
        register_path="data/specs/part_b_registers.pdf",
        intro_path="data/specs/part_c_intro.pdf"
    )
