"""
Generic vLLM OCR implementation via OpenAI-compatible API
Supports any vision-language model served by vLLM
"""

import base64
import requests
from typing import Dict, Any
from PIL import Image
import io
from ..models import OCRSystem


class VLLMOpenAIOCR(OCRSystem):
    """Generic vLLM OCR implementation via OpenAI-compatible API"""
    
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.api_url = config.get('api_url', 'http://localhost:8000/v1/chat/completions')
        self.hf_model_name = config.get('hf_model_name')
        
        if not self.hf_model_name:
            raise ValueError("hf_model_name is required for vLLM OCR systems")
    
    def extract_raw_output(self, image_path: str) -> Dict[str, Any]:
        """Extract raw output from vLLM via OpenAI-compatible API"""
        try:
            # Read and encode image to base64
            with Image.open(image_path).convert('RGB') as img:
                buf = io.BytesIO()
                img.save(buf, format='PNG')
                image_b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
            
            # Prepare payload
            prompt = self.config.get('prompt', 'Extract all visible text from this document image. Return only the text')
            
            payload = {
                'model': self.hf_model_name,
                'messages': [
                    {
                        'role': 'user',
                        'content': [
                            {'type': 'text', 'text': prompt},
                            {'type': 'image_url', 'image_url': {'url': f'data:image/png;base64,{image_b64}'}}
                        ]
                    }
                ],
                'max_tokens': self.config.get('max_tokens', 1024),
                'temperature': self.config.get('temperature', 0.0)
            }
            
            # Call vLLM API
            response = requests.post(self.api_url, json=payload, timeout=120)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            print(f"Error extracting raw output with vLLM ({self.hf_model_name}): {e}")
            return {}

