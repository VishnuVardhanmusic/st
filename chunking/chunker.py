# module2/chunker.py

from typing import List, Dict
from chunking.grouper import group_by_sections


def chunk_labeled_blocks(blocks: List[Dict]) -> List[Dict]:
    """
    Orchestrates the chunking process.
    Groups blocks into sections using heading labels and heuristics.
    Returns a list of section dictionaries.
    """
    sections = group_by_sections(blocks)
    return sections
