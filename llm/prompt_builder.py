# module3/prompt_builder.py

from typing import Dict


def build_prompt(section: Dict, task_type: str = "pseudo") -> str:
    """
    Build an LLM prompt from a structured section.

    Parameters:
        section: Dict containing title, content, etc.
        task_type: "pseudo" or "code" – determines prompt style.

    Returns:
        A full prompt string ready to be passed to the LLM.
    """
    title = section["title"]
    content_blocks = section["content"]
    section_text = " ".join(block["text"] for block in content_blocks)

    if task_type == "pseudo":
        instruction = (
            "You are an expert embedded software engineer. Based on the following technical description, "
            "generate a high-level pseudo code or structured logical flow that helps initialize and control the UART peripheral."
        )
    elif task_type == "code":
        instruction = (
            "You are an embedded C developer. Based on the following documentation, generate complete C code "
            "including initialization routines, register writes, and proper function structure for the UART peripheral "
            "used in the MSPM0 device family."
        )
    else:
        raise ValueError("Unsupported task_type. Use 'pseudo' or 'code'.")

    prompt = f"""
### Instruction:
{instruction}

### Peripheral Context:
Title: {title}
Pages: {section['page_start']}–{section['page_end']}
Source File: {section['source']}

### Technical Description:
{section_text}

### Output Format:
{get_format_hint(task_type)}
""".strip()

    return prompt


def get_format_hint(task_type: str) -> str:
    if task_type == "pseudo":
        return (
            "- Use numbered steps or structured pseudocode blocks\n"
            "- Mention register names if possible\n"
            "- Avoid C/C++ syntax unless necessary"
        )
    elif task_type == "code":
        return (
            "- Provide valid C syntax\n"
            "- Include header and source separation if needed\n"
            "- Use comments to explain important logic\n"
            "- Stick to MSPM0 register names and bitfields as per documentation"
        )
