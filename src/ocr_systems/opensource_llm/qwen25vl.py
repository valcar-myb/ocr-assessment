"""
Qwen2.5-VL Multimodal LLM implementation
"""

import torch
from transformers import Qwen2VLForConditionalGeneration, AutoTokenizer
from PIL import Image
from typing import List
from .models import OCRSystem

class Qwen25VLOCR(OCRSystem):
    """Qwen2.5-VL Multimodal LLM OCR implementation"""
    
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.model_name = config.get('model_name', 'Qwen/Qwen2.5-VL-3B-Instruct')
        self.device = config.get('device', 'cuda' if torch.cuda.is_available() else 'cpu')
        
        # Load model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = Qwen2VLForConditionalGeneration.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16 if self.device == 'cuda' else torch.float32,
            device_map=self.device
        )
        
        # OCR-specific prompt
        self.ocr_prompt = config.get('ocr_prompt', 
            "Please extract all text from this image and return it as plain text.")
    
    def extract_text(self, image_path: str) -> str:
        """Extract text from single image using Qwen2.5-VL"""
        try:
            # Load image
            image = Image.open(image_path).convert('RGB')
            
            # Prepare messages
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "image": image},
                        {"type": "text", "text": self.ocr_prompt}
                    ]
                }
            ]
            
            # Apply chat template
            text = self.tokenizer.apply_chat_template(
                messages, 
                tokenize=False, 
                add_generation_prompt=True
            )
            
            # Tokenize
            inputs = self.tokenizer(text, return_tensors="pt").to(self.device)
            
            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=512,
                    temperature=0.1,
                    do_sample=True
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract generated text
            generated_text = response[len(text):].strip()
            
            return generated_text
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
