import json
import logging
from jinja2 import Environment, FileSystemLoader
from pathlib import Path

# ────────────────
# Logger setup
# ────────────────
logging.basicConfig(level=logging.INFO, format="🧩 [%(levelname)s] %(message)s")

# ────────────────
# Prompt Builder
# ────────────────
def build_pseudo_prompt(
    peripheral_name: str,
    device_family: str,
    overview_text: str,
    operations_text: str,
    register_map: dict,
    intro_text: str
) -> str:
    """
    Builds the LLM prompt using all 3 part inputs and template.
    """
    try:
        env = Environment(loader=FileSystemLoader("prompt_engine/templates"))
        template = env.get_template("pseudo_template.jinja2")

        # Combine overview + operations
        combined_text = f"{overview_text}\n\n{operations_text}"

        prompt = template.render(
            peripheral_name=peripheral_name,
            device_family=device_family,
            overview_text=combined_text.strip(),
            register_json=json.dumps(register_map, indent=2),
            intro_text=intro_text.strip()
        )

        logging.info("Pseudo-code prompt successfully created.")
        return prompt

    except Exception as e:
        logging.error(f"Prompt building failed: {e}")
        return ""
