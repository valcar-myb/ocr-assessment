"""
OCR systems registration and initialization
"""

from .models import OCRSystemFactory

# Import from organized modules
from .opensource_ocr.doctr import DocTROCR
from .opensource_ocr.paddleocr import PaddleOCROCR
from .opensource_ocr.tesseract import TesseractOCR

from .commercial_ocr.aws_textract import AWSTextractOCR
from .commercial_ocr.azure_vision import AzureVisionOCR
from .commercial_ocr.azure_document import AzureDocumentOCR
from .commercial_ocr.google_vision import GoogleVisionOCR
from .commercial_ocr.google_document import GoogleDocumentOCR

from .commercial_llm.gpt4o import GPT4oOCR
from .commercial_llm.gemini_flash import GeminiFlashOCR
from .commercial_llm.claude_haiku import ClaudeHaikuOCR
from .commercial_llm.mistral_ocr import MistralOCR

from .opensource_llm.vllm_openai import VLLMOpenAIOCR

# Register all available OCR systems
OCRSystemFactory.register_system('doctr', DocTROCR)
OCRSystemFactory.register_system('paddleocr', PaddleOCROCR)
OCRSystemFactory.register_system('tesseract', TesseractOCR)

OCRSystemFactory.register_system('aws_textract', AWSTextractOCR)
OCRSystemFactory.register_system('azure_vision', AzureVisionOCR)
OCRSystemFactory.register_system('azure_document', AzureDocumentOCR)
OCRSystemFactory.register_system('google_vision', GoogleVisionOCR)
OCRSystemFactory.register_system('google_document', GoogleDocumentOCR)

OCRSystemFactory.register_system('gpt4o', GPT4oOCR)
OCRSystemFactory.register_system('claude_haiku', ClaudeHaikuOCR)
OCRSystemFactory.register_system('gemini_flash', GeminiFlashOCR)
OCRSystemFactory.register_system('mistral_ocr', MistralOCR)

# Open-source LLMs via vLLM - same class, different models in config
OCRSystemFactory.register_system('qwen25vl', VLLMOpenAIOCR)
OCRSystemFactory.register_system('gemma3', VLLMOpenAIOCR)





def get_ocr_system(name: str, config: dict):
    """Get OCR system instance"""
    return OCRSystemFactory.create_system(name, config)

def get_available_systems():
    """Get list of available OCR systems"""
    return OCRSystemFactory.get_available_systems()