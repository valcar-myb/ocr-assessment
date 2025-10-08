"""
Microsoft Azure Document Intelligence OCR implementation
"""

import requests
import json
from typing import List
from .models import OCRSystem

class AzureDocumentOCR(OCRSystem):
    """Microsoft Azure Document Intelligence OCR implementation"""
    
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.endpoint = config.get('endpoint')
        self.api_key = config.get('api_key')
        self.model_id = config.get('model_id', 'prebuilt-read')
        
        if not self.endpoint or not self.api_key:
            raise ValueError("Azure endpoint and api_key are required")
    
    def extract_text(self, image_path: str) -> str:
        """Extract text from single image using Azure Document Intelligence"""
        try:
            # Read image
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
            
            # Prepare request
            url = f"{self.endpoint}/formrecognizer/documentModels/{self.model_id}:analyze"
            headers = {
                'Ocp-Apim-Subscription-Key': self.api_key,
                'Content-Type': 'application/octet-stream'
            }
            
            # Make request
            response = requests.post(url, headers=headers, data=image_data)
            response.raise_for_status()
            
            # Get operation location
            operation_location = response.headers.get('Operation-Location')
            if not operation_location:
                raise ValueError("No operation location returned")
            
            # Poll for results
            import time
            while True:
                result_response = requests.get(operation_location, headers={'Ocp-Apim-Subscription-Key': self.api_key})
                result_response.raise_for_status()
                result = result_response.json()
                
                if result.get('status') == 'succeeded':
                    break
                elif result.get('status') == 'failed':
                    raise ValueError(f"Analysis failed: {result.get('error', {}).get('message', 'Unknown error')}")
                
                time.sleep(1)
            
            # Extract text
            text_lines = []
            if 'analyzeResult' in result and 'pages' in result['analyzeResult']:
                for page in result['analyzeResult']['pages']:
                    for line in page.get('lines', []):
                        text_lines.append(line.get('content', ''))
            
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
