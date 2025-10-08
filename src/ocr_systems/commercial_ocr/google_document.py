"""
Google Cloud Document AI OCR implementation
"""

import json
from google.cloud import documentai
from typing import List
from .models import OCRSystem

class GoogleDocumentOCR(OCRSystem):
    """Google Cloud Document AI OCR implementation"""
    
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.project_id = config.get('project_id')
        self.location = config.get('location', 'us')
        self.processor_id = config.get('processor_id')
        
        if not self.project_id or not self.processor_id:
            raise ValueError("Google project_id and processor_id are required")
        
        self.client = documentai.DocumentProcessorServiceClient()
        self.processor_name = f"projects/{self.project_id}/locations/{self.location}/processors/{self.processor_id}"
    
    def extract_text(self, image_path: str) -> str:
        """Extract text from single image using Google Document AI"""
        try:
            # Read image
            with open(image_path, 'rb') as image_file:
                image_content = image_file.read()
            
            # Create document
            raw_document = documentai.RawDocument(
                content=image_content,
                mime_type='image/jpeg'
            )
            
            # Process document
            request = documentai.ProcessRequest(
                name=self.processor_name,
                raw_document=raw_document
            )
            
            result = self.client.process_document(request=request)
            document = result.document
            
            # Extract text
            return document.text
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
