# parser/classifier.py

from typing import List, Dict
from config import parser_config as cfg


def classify_text_blocks(blocks: List[Dict]) -> List[Dict]:
    """
    Assigns a label to each text block based on font size, text patterns, and content.
    Returns the modified block list with an added 'label' key.
    """
    labeled_blocks = []

    for block in blocks:
        text = block["text"]
        size = block["size"]
        label = cfg.LABEL_MISC

        if text.isupper() and size >= cfg.FONT_SIZE_THRESHOLD_HEADING:
            label = cfg.LABEL_SECTION
        elif size >= cfg.FONT_SIZE_THRESHOLD_HEADING:
            label = cfg.LABEL_SECTION
        elif size >= cfg.FONT_SIZE_THRESHOLD_SUBHEADING:
            label = cfg.LABEL_SUBSECTION
        elif text.startswith(("-", "*", "•")) or text.strip()[0:2].isdigit():
            label = cfg.LABEL_BULLET
        elif any(kw in text.lower() for kw in cfg.REGISTER_KEYWORDS) and len(text.split()) <= 8:
            label = cfg.LABEL_TABLE_ROW
        else:
            label = cfg.LABEL_PARAGRAPH

        block["label"] = label
        labeled_blocks.append(block)

    return labeled_blocks
