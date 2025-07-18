# main_chunking.py

import json
from pathlib import Path
from chunking.chunker import chunk_labeled_blocks

INPUT_JSON = Path("output/extracted_blocks.json")

CHUNKED_OUTPUT = Path("output/structured_sections.json")


def load_labeled_blocks(filepath: Path):
    """Load labeled blocks from JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def save_sections(sections, filepath: Path):
    """Save structured sections to JSON."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(sections, f, indent=2, ensure_ascii=False)


def preview_sections(sections, n=3):
    print("\n📚 Previewing Chunked Sections:\n" + "-" * 40)
    for i, section in enumerate(sections[:n]):
        print(f"[{i+1}] Title: {section['title']}")
        print(f"Source: {section['source']}, Pages: {section['page_start']}–{section['page_end']}")
        print(f"Content Blocks: {len(section['content'])}")
        print(f"First Block: {section['content'][0]['text'][:80]}...\n")


def main():
    print("📂 Loading labeled blocks...")
    labeled_blocks = load_labeled_blocks(INPUT_JSON)

    print("🔧 Chunking into sections...")
    sections = chunk_labeled_blocks(labeled_blocks)

    print("💾 Saving structured sections...")
    save_sections(sections, CHUNKED_OUTPUT)

    preview_sections(sections, n=5)
    print(f"\n✅ Chunking complete. Output saved to: {CHUNKED_OUTPUT.resolve()}")


if __name__ == "__main__":
    main()
