import pdf2image
import pytesseract
from PIL import Image
from PyPDF2 import PdfReader

def text_extraction(pdf_path,dpi):
    images = pdf2image.convert_from_path(pdf_path,dpi)

    full_text = ""
    for i, img in enumerate(images):
        text = pytesseract.image_to_string(img, lang='eng')
        full_text += f"\n--- Page {i+1} ---\n{text}"
    
    return full_text