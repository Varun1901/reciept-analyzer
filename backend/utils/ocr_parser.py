import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from PIL import Image

# If Tesseract is not in PATH, set it manually (update if needed)
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_path: str) -> str:
    """Extract raw text from an image using Tesseract OCR"""
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text
