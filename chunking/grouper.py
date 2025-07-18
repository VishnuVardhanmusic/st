from typing import List, Dict


def group_by_sections(blocks: List[Dict]) -> List[Dict]:
    """
    Groups labeled blocks into sections based on SECTION_HEADING or SUBSECTION.
    Each section contains a list of its paragraphs, bullets, and tables.
    """
    sections = []
    current_section = {
        "title": "Untitled",
        "source": "",
        "page_start": None,
        "page_end": None,
        "content": []
    }

    for block in blocks:
        label = block.get("label")
        text = block["text"]
        page = block["page"]
        origin = block["origin"]

        # When a new heading is detected, push old section and start new
        if label in ("SECTION_HEADING", "SUBSECTION"):
            if current_section["content"]:
                current_section["page_end"] = page
                sections.append(current_section)

            current_section = {
                "title": text,
                "source": origin,
                "page_start": page,
                "page_end": page,
                "content": []
            }
        else:
            current_section["content"].append({
                "text": text,
                "label": label,
                "font": block.get("font"),
                "size": block.get("size"),
                "page": page
            })

    # Add the last section
    if current_section["content"]:
        sections.append(current_section)

    return sections
