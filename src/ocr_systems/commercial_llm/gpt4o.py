"""
GPT-4o Commercial LLM implementation
"""

import openai
import base64
from typing import List
from .models import OCRSystem

class GPT4oOCR(OCRSystem):
    """GPT-4o Commercial LLM OCR implementation"""
    
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.api_key = config.get('api_key')
        self.model = config.get('model', 'gpt-4o')
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        
        # OCR-specific prompt
        self.ocr_prompt = config.get('ocr_prompt', 
            "Extract all text from this image. Return only the text content without any additional formatting or explanation.")
    
    def extract_text(self, image_path: str) -> str:
        """Extract text from single image using GPT-4o"""
        try:
            # Encode image
            with open(image_path, 'rb') as image_file:
                base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": self.ocr_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000,
                temperature=0.1
            )
            
            return response.choices[0].message.content.strip()
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
