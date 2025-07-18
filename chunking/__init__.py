"""
Module 2: Semantic Chunking and Section Reconstructor

This module reads labeled PDF text blocks (output of Module 1) and:
1. Detects section boundaries using heading labels and font sizes.
2. Groups relevant paragraphs, tables, and bullets under each section.
3. Merges and formats sections for easy LLM consumption and code generation.
"""
