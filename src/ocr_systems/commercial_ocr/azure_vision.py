"""
Microsoft Azure AI Vision OCR implementation
"""

import requests
import base64
import json
from typing import List
from .models import OCRSystem

class AzureVisionOCR(OCRSystem):
    """Microsoft Azure AI Vision OCR implementation"""
    
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.endpoint = config.get('endpoint')
        self.api_key = config.get('api_key')
        self.version = config.get('version', '2023-02-01-preview')
        
        if not self.endpoint or not self.api_key:
            raise ValueError("Azure endpoint and api_key are required")
    
    def extract_text(self, image_path: str) -> str:
        """Extract text from single image using Azure Vision API"""
        try:
            # Read image and encode
            with open(image_path, 'rb') as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Prepare request
            url = f"{self.endpoint}/vision/v4.0/ocr"
            headers = {
                'Ocp-Apim-Subscription-Key': self.api_key,
                'Content-Type': 'application/json'
            }
            
            body = {
                'url': f"data:image/jpeg;base64,{image_data}"
            }
            
            # Make request
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()
            
            # Parse response
            result = response.json()
            
            # Extract text
            text_lines = []
            if 'regions' in result:
                for region in result['regions']:
                    for line in region.get('lines', []):
                        line_text = ' '.join([word.get('text', '') for word in line.get('words', [])])
                        text_lines.append(line_text)
            
            return ' '.join(text_lines)
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
