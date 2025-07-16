import os
import logging
from time import sleep
from dotenv import load_dotenv
import litellm

# ────────────────
# Setup
# ────────────────
load_dotenv()
logging.basicConfig(level=logging.INFO, format="🤖 [%(levelname)s] %(message)s")

MODEL = os.getenv("MODEL_NAME", "gpt-4")
BASE_URL = os.getenv("LITELLM_BASE_URL")
API_KEY = os.getenv("LITELLM_API_KEY")
MAX_RETRIES = 3


def call_llm(prompt: str, temperature: float = 0.2) -> str:
    """
    Sends a prompt to LLM via LiteLLM proxy and returns the generated content.
    """
    if not prompt.strip():
        logging.error("Empty prompt string.")
        return ""

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logging.info(f"Attempt {attempt}: Sending prompt to model [{MODEL}]...")

            response = litellm.completion(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "You are an embedded systems assistant who generates register-level C code."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                api_base=BASE_URL,
                api_key=API_KEY
            )

            if response and "choices" in response and response["choices"]:
                content = response["choices"][0]["message"]["content"]
                if content.strip():
                    logging.info("LLM response received successfully.")
                    return content

        except Exception as e:
            logging.warning(f"⚠️ Attempt {attempt} failed: {e}")
            sleep(1 + attempt)  # simple backoff

    logging.error("All LLM attempts failed. Returning empty result.")
    return ""
