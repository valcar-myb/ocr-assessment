"""
DocTR OCR implementation
"""

from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import torch
import time
from typing import List, Dict, Any, Tuple
from ocr_systems.models import OCRSystem

class DocTROCR(OCRSystem):
    """DocTR OCR system implementation"""
    
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.det_arch = config.get('det_arch', 'db_resnet50')
        self.reco_arch = config.get('reco_arch', 'crnn_vgg16_bn')
        self.pretrained = config.get('pretrained', True)
        self.device = config.get('device', 'cuda' if torch.cuda.is_available() else 'cpu')
        
        # Initialize DocTR predictor
        self.predictor = ocr_predictor(
            det_arch=self.det_arch,
            reco_arch=self.reco_arch,
            pretrained=self.pretrained
        ).to(self.device)
    
    def extract_text(self, image_path: str) -> str:
        """Extract text from single image using DocTR"""
        try:
            # Load image
            doc = DocumentFile.from_images(image_path)
            
            # Run OCR
            result = self.predictor(doc)
            
            # Extract text from result using the same logic as parse_raw_output
            pages = result.export().get("prediction", {}).get("pages", [])
            
            words = []
            for page in pages:
                for block in page.get("blocks", []):
                    for line in block.get("lines", []):
                        for word in line.get("words", []):
                            words.append(word["value"])
            
            return ' '.join(words)
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            return ""
    
    def extract_raw_output(self, image_path: str) -> Dict[str, Any]:
        """Extract raw DocTR output from image"""
        # Load image
        doc = DocumentFile.from_images(image_path)
        
        # Run OCR
        result = self.predictor(doc)
        
        # Return raw result export
        return result.export()
    
    def batch_extract(self, image_paths: List[str]) -> List[str]:
        """Extract text from multiple images"""
        results = []
        for image_path in image_paths:
            text = self.extract_text(image_path)
            results.append(text)
        return results
    
    def parse_raw_output(self, raw_data: Dict[str, Any]) -> str:
        """Parse DocTR raw output and return extracted text"""
        try:
            text_lines = []
            for page in raw_data.get('pages', []):
                for block in page.get('blocks', []):
                    for line in block.get('lines', []):
                        # Extract words from line
                        words = []
                        for word in line.get('words', []):
                            if isinstance(word, dict) and 'value' in word:
                                words.append(word['value'])
                        if words:
                            text_lines.append(' '.join(words))
            
            return '\n'.join(text_lines)
        except Exception as e:
            print(f"Error parsing DocTR raw output: {e}")
            return ""
