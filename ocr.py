from PIL import Image
import pytesseract

from utils import clean_ocr_text


def image_to_text(image_path: str) -> str:
    """Extract text from an image using Tesseract OCR."""
    try:
        raw_text = pytesseract.image_to_string(Image.open(image_path))
        return clean_ocr_text(raw_text)
    except Exception as exc:
        raise RuntimeError(f"OCR failed: {exc}")

