"""
AWS Textract OCR implementation
"""

import boto3
import json
from typing import List
from .models import OCRSystem

class AWSTextractOCR(OCRSystem):
    """AWS Textract OCR implementation"""
    
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.region_name = config.get('region_name', 'us-east-1')
        self.aws_access_key_id = config.get('aws_access_key_id')
        self.aws_secret_access_key = config.get('aws_secret_access_key')
        
        # Initialize Textract client
        if self.aws_access_key_id and self.aws_secret_access_key:
            self.client = boto3.client(
                'textract',
                region_name=self.region_name,
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key
            )
        else:
            # Use default credentials
            self.client = boto3.client('textract', region_name=self.region_name)
    
    def extract_text(self, image_path: str) -> str:
        """Extract text from single image using AWS Textract"""
        try:
            # Read image
            with open(image_path, 'rb') as image_file:
                image_bytes = image_file.read()
            
            # Call Textract
            response = self.client.detect_document_text(
                Document={'Bytes': image_bytes}
            )
            
            # Extract text
            text_lines = []
            for block in response['Blocks']:
                if block['BlockType'] == 'LINE':
                    text_lines.append(block['Text'])
            
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
