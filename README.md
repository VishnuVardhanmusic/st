pip install litellm jinja2 pdfplumber python-dotenv pandas tqdm

| Package                | Why It's Needed                                        |
| ---------------------- | ------------------------------------------------------ |
| `litellm`              | Core LLM API abstraction (Claude, GPT, Ollama, etc.)   |
| `jinja2`               | Templating for prompt construction and code generation |
| `pypdf` / `pdfplumber` | Reliable PDF content extraction (text/tables)          |
| `python-dotenv`        | Store and load API keys securely                       |
| `tqdm`                 | Progress bars, async task visibility                   |
| `pandas`               | Register table parsing if needed                       |
| `asyncio`              | Parallel LLM calls when required                       |
| `re` (built-in)        | Regex for extracting code blocks                       |
| `os`, `pathlib`        | File operations                                        |
| `logging`              | Structured error and response logs                     |
