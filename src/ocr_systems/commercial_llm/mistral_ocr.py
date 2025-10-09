"""
Mistral OCR Vision implementation
"""

import base64
from typing import Dict, Any
from ..models import OCRSystem


class MistralOCR(OCRSystem):
    """Mistral OCR implementation"""
    
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.model = None
        self._init_predictor()
    
    def _init_predictor(self):
        """Initialize Mistral client"""
        try:
            from mistralai import Mistral
            
            self.model = Mistral(
                api_key=self.config.get('api_key')
            )
        except ImportError:
            print("Mistral AI package not installed. Please install with: pip install mistralai")
            raise
        except Exception as e:
            print(f"Error initializing Mistral client: {e}")
            raise
    
    def extract_raw_output(self, image_path: str) -> Dict[str, Any]:
        """Extract raw output from Mistral OCR"""
        try:
            # Read and encode image
            with open(image_path, 'rb') as img_file:
                img = base64.b64encode(img_file.read()).decode('utf-8')
            
            # Call Mistral OCR API
            ocr_response = self.model.ocr.process(
                model=self.config.get('model', 'pixtral-12b-2409'),
                document={
                    'type': 'image_url',
                    'image_url': f'data:image/jpeg;base64,{img}'
                }
            )
            
            return ocr_response.model_dump()
        except Exception as e:
            print(f"Error extracting raw output with Mistral OCR: {e}")
            return {}
