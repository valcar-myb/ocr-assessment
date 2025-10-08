"""
OCR output parsers - one method per OCR system
"""

from typing import Dict, Any


class OCRParser:
    """Parser for OCR raw outputs"""
    
    @staticmethod
    def parse_doctr(raw_data: Dict[str, Any]) -> str:
        """Parse DocTR raw output and return extracted text"""
        text_lines = []
        for page in raw_data.get('pages', []):
            for block in page.get('blocks', []):
                for line in block.get('lines', []):
                    words = []
                    for word in line.get('words', []):
                        if isinstance(word, dict) and 'value' in word:
                            words.append(word['value'])
                    if words:
                        text_lines.append(' '.join(words))
        
        return ' '.join(text_lines)
    
    @staticmethod
    def parse_paddleocr(raw_data: Dict[str, Any]) -> str:
        """Parse PaddleOCR raw output and return extracted text"""
        rec_texts = raw_data.get('rec_texts', [])
        if rec_texts:
            return " ".join(rec_texts)
        return ""
    
    @staticmethod
    def parse_tesseract(raw_data: Dict[str, Any]) -> str:
        """Parse Tesseract raw output and return extracted text"""
        # Tesseract raw output is typically just text
        return raw_data.get('text', '')
    
    @staticmethod
    def parse_easyocr(raw_data: Dict[str, Any]) -> str:
        """Parse EasyOCR raw output and return extracted text"""
        texts = []
        results = raw_data.get('results', [])
        for result in results:
            if isinstance(result, list) and len(result) >= 2:
                # EasyOCR format: [[bbox], text, confidence]
                texts.append(result[1])
        return " ".join(texts)
    
    @staticmethod
    def get_parser(system_name: str):
        """Get parser function for specific OCR system"""
        parsers = {
            'doctr': OCRParser.parse_doctr,
            'paddleocr': OCRParser.parse_paddleocr,
            'tesseract': OCRParser.parse_tesseract,
            'easyocr': OCRParser.parse_easyocr,
        }
        
        return parsers.get(system_name, lambda x: "")
