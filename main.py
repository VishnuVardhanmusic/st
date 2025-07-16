import argparse
from generator.pseudo_codegen import generate_pseudocode
from generator.full_codegen import generate_final_code
from pathlib import Path
import logging

# ────────────────
# Logger setup
# ────────────────
logging.basicConfig(level=logging.INFO, format="📦 [%(levelname)s] %(message)s")


def run_pipeline(peripheral_name: str, device_family: str):
    """
    Orchestrates full pseudocode and final code generation pipeline.
    """

    logging.info(f"🚀 Generating code for {peripheral_name} on device {device_family}")

    # File paths
    base_path = Path("data/specs")
    trm_pdf = base_path / "part_a_trm.pdf"
    register_pdf = base_path / "part_b_registers.pdf"
    intro_pdf = base_path / "part_c_intro.pdf"

    # Phase 1: Pseudocode
    generate_pseudocode(
        peripheral_name=peripheral_name,
        device_family=device_family,
        trm_path=str(trm_pdf),
        register_path=str(register_pdf),
        intro_path=str(intro_pdf)
    )

    # Phase 2: Final Code
    pseudo_code_path = Path(f"outputs/pseudocode/{peripheral_name.lower()}_pseudo.c")

    generate_final_code(
        peripheral_name=peripheral_name,
        device_family=device_family,
        trm_path=str(trm_pdf),
        register_path=str(register_pdf),
        intro_path=str(intro_pdf),
        pseudo_code_path=str(pseudo_code_path)
    )


# ────────────────
# CLI Entry Point
# ────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="📡 MCU Code Generation Assistant")
    parser.add_argument("--peripheral", required=True, help="Peripheral name (e.g. UART0)")
    parser.add_argument("--device", required=True, help="Device family name (e.g. MSPM0G3507)")
    args = parser.parse_args()

    run_pipeline(args.peripheral, args.device)
