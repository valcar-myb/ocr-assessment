"""
Gemini 2.0 Flash Commercial LLM implementation
"""

import google.generativeai as genai
from PIL import Image
from typing import List
from .models import OCRSystem

class GeminiFlashOCR(OCRSystem):
    """Gemini 2.0 Flash Commercial LLM OCR implementation"""
    
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.api_key = config.get('api_key')
        self.model_name = config.get('model_name', 'gemini-2.0-flash-exp')
        
        if not self.api_key:
            raise ValueError("Google API key is required")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
        
        # OCR-specific prompt
        self.ocr_prompt = config.get('ocr_prompt', 
            "Extract all text from this image. Return only the text content without any additional formatting or explanation.")
    
    def extract_text(self, image_path: str) -> str:
        """Extract text from single image using Gemini 2.0 Flash"""
        try:
            # Load image
            image = Image.open(image_path)
            
            # Generate content
            response = self.model.generate_content([
                self.ocr_prompt,
                image
            ])
            
            return response.text.strip()
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
