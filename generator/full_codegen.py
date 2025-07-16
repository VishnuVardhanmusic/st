import os
import logging
from pathlib import Path

from parsers.trm_parser import parse_trm
from parsers.register_parser import parse_register_pdf
from parsers.intro_parser import parse_intro_pdf
from llm_engine.call_llm import call_llm
from llm_engine.extract_code import extract_c_code_block

# ────────────────
# Logger Setup
# ────────────────
logging.basicConfig(level=logging.INFO, format="🔧 [%(levelname)s] %(message)s")

def generate_final_code(
    peripheral_name: str,
    device_family: str,
    trm_path: str,
    register_path: str,
    intro_path: str,
    pseudo_code_path: str
):
    """
    Final phase: Generate full C code from pseudocode + original specs
    """
    logging.info("🚀 Starting final code generation pipeline...")

    # 1. Load pseudocode
    if not Path(pseudo_code_path).exists():
        logging.error(f"Pseudocode file not found: {pseudo_code_path}")
        return

    with open(pseudo_code_path, "r") as f:
        pseudocode = f.read().strip()

    if not pseudocode:
        logging.error("Pseudocode file is empty.")
        return

    # 2. Parse all 3 parts again
    trm_data = parse_trm(trm_path)
    register_data = parse_register_pdf(register_path)
    intro_text = parse_intro_pdf(intro_path)

    # 3. Build final prompt
    prompt = f"""
You are a C embedded systems engineer.
Your task is to convert pseudocode into real C code for {peripheral_name} on {device_family}.

📘 General Notes from Engineers:
{intro_text.strip()}

🧠 Peripheral Overview:
{trm_data.get('overview', '').strip()}

🛠️ Operations:
{trm_data.get('operations', '').strip()}

📦 Register Info:
{register_data}

✏️ Pseudocode:
```c
{pseudocode}
 Now generate valid C code implementing the logic from the pseudocode, using exact register names, access rules, and init sequences.
Keep inline comments and include proper headers, macros, and error checks.
Return only the code in a valid ```c block.
"""

# 4. Call LLM
llm_response = call_llm(prompt)

# 5. Extract final code
final_code = extract_c_code_block(llm_response)

# 6. Save result
output_dir = Path("outputs/fullcode")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / f"{peripheral_name.lower()}_final.c"
with open(output_file, "w") as f:
    f.write(final_code)

logging.info(f"✅ Final C code saved to {output_file}")


## ✅ CLI Trigger (for local testing)
if __name__ == "__main__":
    generate_final_code(
        peripheral_name="UART0",
        device_family="MSPM0G3507",
        trm_path="data/specs/part_a_trm.pdf",
        register_path="data/specs/part_b_registers.pdf",
        intro_path="data/specs/part_c_intro.pdf",
        pseudo_code_path="outputs/pseudocode/uart0_pseudo.c"
    )
