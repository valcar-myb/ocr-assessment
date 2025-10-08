"""
MistralOCR Commercial LLM implementation
"""

import requests
import base64
import json
from typing import List
from .models import OCRSystem

class MistralOCR(OCRSystem):
    """MistralOCR Commercial LLM implementation"""
    
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.api_key = config.get('api_key')
        self.endpoint = config.get('endpoint', 'https://api.mistral.ai/v1/chat/completions')
        self.model = config.get('model', 'mistral-ocr')
        
        if not self.api_key:
            raise ValueError("Mistral API key is required")
        
        # OCR-specific prompt for structured output
        self.ocr_prompt = config.get('ocr_prompt', 
            "Extract all text from this document image. Return the text content in a structured format preserving the layout.")
    
    def extract_text(self, image_path: str) -> str:
        """Extract text from single image using MistralOCR"""
        try:
            # Encode image
            with open(image_path, 'rb') as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Prepare request
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'model': self.model,
                'messages': [
                    {
                        'role': 'user',
                        'content': [
                            {'type': 'text', 'text': self.ocr_prompt},
                            {
                                'type': 'image_url',
                                'image_url': {
                                    'url': f'data:image/jpeg;base64,{base64_image}'
                                }
                            }
                        ]
                    }
                ],
                'max_tokens': 1000,
                'temperature': 0.1
            }
            
            # Make API call
            response = requests.post(self.endpoint, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
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
