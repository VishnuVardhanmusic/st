# module3/llm_client.py

from litellm import completion
from config.llm_config import BASE_URL, API_KEY, MODEL_NAME


def call_llm(prompt: str, temperature: float = 0.3) -> str:
    """
    Call the LLaMA 3 70B model via LiteLLM proxy using direct function call.

    Parameters:
        prompt: The input prompt string
        temperature: Sampling temperature

    Returns:
        The generated response as plain text
    """
    try:
        response = completion(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            api_key=API_KEY,
            base_url=BASE_URL,
            temperature=temperature,
        )
        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        print(f"❌ LLM call failed: {e}")
        return "[ERROR] Unable to generate response"
