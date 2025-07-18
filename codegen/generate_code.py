# module_full_codegen/generate_uart_code.py

from config.llm_config import MODEL_NAME, API_KEY, BASE_URL
from litellm import completion
from pathlib import Path
import re

from codegen.build_final_prompt import build_final_prompt

OUTPUT_DIR = Path("output/final_uart_code")
HEADER_PATH = OUTPUT_DIR / "uart_driver.h"
SOURCE_PATH = OUTPUT_DIR / "uart_driver.c"
RAW_OUTPUT_PATH = OUTPUT_DIR / "raw_response.txt"


def call_llm(prompt: str) -> str:
    """Send full prompt to LLM and return response."""
    try:
        response = completion(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            api_key=API_KEY,
            base_url=BASE_URL,
            temperature=0.2,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"❌ Error calling LLM: {e}")
        return "[ERROR] LLM failed to respond."


def split_and_save_response(response: str):
    """Split .h and .c blocks and save them separately."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(RAW_OUTPUT_PATH, "w", encoding="utf-8") as raw_file:
        raw_file.write(response)

    # Regex-based boundary detection
    header_match = re.search(r"```c\n(/\*.*?\.h.*?)```", response, re.DOTALL)
    source_match = re.search(r"```c\n(/\*.*?\.c.*?)```", response, re.DOTALL)

    # Save files
    if header_match:
        with open(HEADER_PATH, "w", encoding="utf-8") as h:
            h.write(header_match.group(1).strip())
        print(f"✅ Header saved: {HEADER_PATH}")
    else:
        print("⚠️ Header block not found.")

    if source_match:
        with open(SOURCE_PATH, "w", encoding="utf-8") as c:
            c.write(source_match.group(1).strip())
        print(f"✅ Source saved: {SOURCE_PATH}")
    else:
        print("⚠️ Source block not found.")


def main():
    print("🧠 Building final code generation prompt...")
    prompt = build_final_prompt()

    print("🤖 Sending to Meta LLaMA-3 via LiteLLM...")
    response = call_llm(prompt)

    print("💾 Splitting and saving C output...")
    split_and_save_response(response)

    print("\n✅ UART full code generation completed!")


if __name__ == "__main__":
    main()
