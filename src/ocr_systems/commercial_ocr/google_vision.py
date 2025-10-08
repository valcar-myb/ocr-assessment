"""
Google Cloud Vision OCR implementation
"""

import io
from google.cloud import vision
from typing import List
from .models import OCRSystem

class GoogleVisionOCR(OCRSystem):
    """Google Cloud Vision OCR implementation"""
    
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.client = vision.ImageAnnotatorClient()
        self.language_hints = config.get('language_hints', ['en'])
    
    def extract_text(self, image_path: str) -> str:
        """Extract text from single image using Google Vision API"""
        try:
            with io.open(image_path, 'rb') as image_file:
                content = image_file.read()
            
            image = vision.Image(content=content)
            
            response = self.client.text_detection(
                image=image,
                image_context={'language_hints': self.language_hints}
            )
            
            texts = response.text_annotations
            if texts:
                return texts[0].description.strip()
            return ""
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