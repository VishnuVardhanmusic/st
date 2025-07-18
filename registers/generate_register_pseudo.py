# module_registers/generate_register_pseudo.py

"""
Driver script to:
1. Extract UART register field tables from the PDF
2. Construct a register-level prompt
3. Query LLaMA-3-70B via LiteLLM
4. Save the generated register-aware pseudo code to output
"""

from registers.extract_register_tables import (
    extract_register_tables,
    save_register_data,
    REGISTER_PDF_PATH,
    OUTPUT_JSON_PATH,
)

from registers.register_prompt_llm import (
    build_register_prompt,
    call_llm,
    save_response,
    OUTPUT_TXT
)


def main():
    print("🔍 Extracting register field tables...")
    tables = extract_register_tables(REGISTER_PDF_PATH)
    save_register_data(tables, OUTPUT_JSON_PATH)

    print("🧠 Building register-aware LLM prompt...")
    prompt = build_register_prompt(tables)

    print("🤖 Calling Meta-LLaMA-3 via LiteLLM proxy...")
    response = call_llm(prompt)

    print("💾 Saving pseudo code output...")
    save_response(response, OUTPUT_TXT)

    print("\n✅ Register-level pseudo generation complete!")


if __name__ == "__main__":
    main()
