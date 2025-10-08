"""
Tesseract OCR implementation
"""

import pytesseract
from PIL import Image
from typing import List
from ocr_systems.models import OCRSystem

class TesseractOCR(OCRSystem):
    """Tesseract OCR system implementation"""
    
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.language = config.get('language', 'eng')
        self.psm = config.get('psm', 6)
    
    def extract_text(self, image_path: str) -> str:
        """Extract text from single image using Tesseract"""
        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(
                image, 
                lang=self.language,
                config=f'--psm {self.psm}'
            )
            return text.strip()
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            return ""
    
    def batch_extract(self, image_paths: List[str]) -> List[str]:
        """Extract text from multiple images"""
        results = []
        for image_path in image_paths:
            text = self.extract_text(image_path)
            results.append(text)
        return results
