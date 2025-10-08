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
    
    def extract_raw_output(self, image_path: str) -> Dict[str, Any]:
        """Extract raw DocTR output from image"""
        # Load image
        doc = DocumentFile.from_images(image_path)
        
        # Run OCR
        result = self.predictor(doc)
        
        # Return raw result export
        return result.export()

