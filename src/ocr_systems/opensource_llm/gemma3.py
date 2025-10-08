"""
Gemma 3 Multimodal LLM implementation
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from PIL import Image
from typing import List
from .models import OCRSystem

class Gemma3OCR(OCRSystem):
    """Gemma 3 Multimodal LLM OCR implementation"""
    
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.model_name = config.get('model_name', 'google/gemma-3-4b-instruct')
        self.device = config.get('device', 'cuda' if torch.cuda.is_available() else 'cpu')
        
        # Load model and tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype=torch.float16 if self.device == 'cuda' else torch.float32,
            device_map=self.device
        )
        
        # OCR-specific prompt
        self.ocr_prompt = config.get('ocr_prompt', 
            "Extract all text from this image. Return only the text content without any additional formatting or explanation.")
    
    def extract_text(self, image_path: str) -> str:
        """Extract text from single image using Gemma 3"""
        try:
            # Load image
            image = Image.open(image_path).convert('RGB')
            
            # Prepare input
            messages = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": self.ocr_prompt},
                        {"type": "image", "image": image}
                    ]
                }
            ]
            
            # Tokenize and generate
            inputs = self.tokenizer.apply_chat_template(
                messages, 
                tokenize=True, 
                return_tensors="pt"
            ).to(self.device)
            
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_new_tokens=512,
                    temperature=0.1,
                    do_sample=True
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract text after the prompt
            if "assistant" in response:
                text = response.split("assistant")[-1].strip()
            else:
                text = response.strip()
            
            return text
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
