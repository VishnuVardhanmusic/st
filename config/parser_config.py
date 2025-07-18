# config/parser_config.py

# Font size thresholds to classify heading vs paragraph
FONT_SIZE_THRESHOLD_HEADING = 14
FONT_SIZE_THRESHOLD_SUBHEADING = 12

# Minimum text length to consider a block valid
MIN_TEXT_LENGTH = 5

# Common keywords to detect register-related content
REGISTER_KEYWORDS = [
    "offset", "bit", "access", "reset", "description", "register", "field", "default"
]

# Label types
LABEL_SECTION = "SECTION_HEADING"
LABEL_SUBSECTION = "SUBSECTION"
LABEL_PARAGRAPH = "PARAGRAPH"
LABEL_BULLET = "BULLET_POINT"
LABEL_TABLE_ROW = "TABLE_ROW"
LABEL_MISC = "MISC"

# Output path
EXTRACTION_OUTPUT_PATH = "output/extracted_blocks.json"
