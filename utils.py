import re


def clean_ocr_text(text: str) -> str:
    """Clean OCR output for easier parsing."""
    if not text:
        return ""
    # Replace common OCR mistakes
    cleaned = text.replace("\n", " ")
    cleaned = cleaned.replace("—", "-")
    cleaned = cleaned.replace("O", "0")
    cleaned = cleaned.replace("l", "1")
    # Remove any characters not used in simple calculus expressions
    cleaned = re.sub(r"[^0-9a-zA-Z+\-*/^()= .,\\int\\limd]", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()

