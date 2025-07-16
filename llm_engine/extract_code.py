import re
import logging

# ────────────────
# Logger setup
# ────────────────
logging.basicConfig(level=logging.INFO, format="🧾 [%(levelname)s] %(message)s")


def extract_c_code_block(text: str) -> str:
    """
    Extracts the first C-style code block from LLM output.
    Looks for ```c ... ``` or plain ``` blocks.
    Returns clean C code or empty string.
    """
    if not text:
        logging.warning("Empty LLM output received for code extraction.")
        return ""

    # Pattern to extract fenced code blocks
    code_block_pattern = re.compile(
        r"```(?:c)?\s*\n(.*?)```",
        re.DOTALL | re.IGNORECASE
    )

    match = code_block_pattern.search(text)
    if match:
        code = match.group(1).strip()
        logging.info("✅ C code block successfully extracted.")
        return code
    else:
        logging.warning("⚠️ No fenced C code block found in response.")
        return ""


# ────────────────
# CLI Testing (Optional)
# ────────────────
if __name__ == "__main__":
    sample = """
Here's the generated pseudocode:

```c
#include <stdint.h>

void init_uart() {
  UARTCTL |= (1 << ENABLE_BIT);
  UARTBAUD = 0x1A;
}
"""