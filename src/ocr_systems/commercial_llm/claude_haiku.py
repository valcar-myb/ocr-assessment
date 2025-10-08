"""
Claude 3.5 Haiku Commercial LLM implementation
"""

import anthropic
import base64
from typing import List
from .models import OCRSystem

class ClaudeHaikuOCR(OCRSystem):
    """Claude 3.5 Haiku Commercial LLM OCR implementation"""
    
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.api_key = config.get('api_key')
        self.model = config.get('model', 'claude-3-5-haiku-20241022')
        
        if not self.api_key:
            raise ValueError("Anthropic API key is required")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        
        # OCR-specific prompt
        self.ocr_prompt = config.get('ocr_prompt', 
            "Extract all text from this image. Return only the text content without any additional formatting or explanation.")
    
    def extract_text(self, image_path: str) -> str:
        """Extract text from single image using Claude 3.5 Haiku"""
        try:
            # Encode image
            with open(image_path, 'rb') as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Make API call
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.1,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": self.ocr_prompt},
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": image_data
                                }
                            }
                        ]
                    }
                ]
            )
            
            return response.content[0].text.strip()
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
