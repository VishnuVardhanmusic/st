# parser/utils.py

import json
from pathlib import Path
from typing import List, Dict


def save_blocks_to_json(blocks: List[Dict], output_path: Path):
    """
    Saves the list of labeled or extracted blocks to a JSON file.
    Creates parent folders if they don't exist.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(blocks, f, indent=2, ensure_ascii=False)


def preview_blocks(blocks: List[Dict], n: int = 5):
    """
    Prints a preview of the first few labeled blocks for inspection.
    """
    print(f"\nPreviewing first {n} blocks:\n" + "-"*40)
    for i, block in enumerate(blocks[:n]):
        print(f"[{i+1}] ({block['origin']} - Page {block['page']})")
        print(f"Label: {block.get('label', 'N/A')}")
        print(f"Text : {block['text'][:100]}...\n")
