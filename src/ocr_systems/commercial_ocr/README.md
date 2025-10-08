# Commercial OCR Systems

This directory contains implementations of commercial OCR systems for the benchmark.

## Implemented Systems

| System | Provider | Region/Location | Model/Version | Document OCR |
|--------|----------|-----------------|---------------|:------------:|
| **AWS Textract** | Amazon Web Services | `eu-central-1` | Default (latest) | ✓ |
| **Azure Vision** | Microsoft Azure | West Europe | `latest` | ✗ |
| **Azure Document Intelligence** | Microsoft Azure | West Europe | `prebuilt-read` | ✓ |
| **Google Vision** | Google Cloud Platform | Global | Text Detection API | ✗ |
| **Google Document AI** | Google Cloud Platform | `eu` (Europe) | Document OCR Processor | ✓ |

## Configuration Details

### AWS Textract
- **Region**: `eu-central-1` (Europe - Frankfurt)
- **API**: `detect_document_text`
- **Authentication**: AWS credentials (IAM)

### Azure Vision
- **Service**: Azure AI Vision (Computer Vision)
- **Endpoint**: `https://ocr-benchmark-myb.cognitiveservices.azure.com/`
- **Model Version**: `latest`
- **API**: Image Analysis READ

### Azure Document Intelligence
- **Service**: Azure AI Document Intelligence (formerly Form Recognizer)
- **Endpoint**: `https://ocr-bench-doc-intelligence.cognitiveservices.azure.com/`
- **Model**: `prebuilt-read`
- **API**: Document Analysis

### Google Vision
- **Service**: Cloud Vision API
- **Project ID**: `api-ocr-355407`
- **API**: Text Detection
- **Location**: Global (no specific region)
- **Service Account**: `benchmark-ocr@api-ocr-355407.iam.gserviceaccount.com`

### Google Document AI
- **Service**: Cloud Document AI
- **Project ID**: `api-ocr-355407`
- **Location**: `eu` (Europe)
- **Processor ID**: `5a7955cb49e39a00`
- **Processor Type**: Document OCR
- **Service Account**: `test-ocr-api@api-ocr-355407.iam.gserviceaccount.com`

## Architecture

All commercial OCR implementations follow the same pattern:

```python
class CommercialOCR(OCRSystem):
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.model = None
        self._init_predictor()
    
    def _init_predictor(self):
        """Initialize the commercial API client"""
        # Setup authentication and client
        pass
    
    def extract_raw_output(self, image_path: str) -> Dict[str, Any]:
        """Extract raw output from the commercial OCR API"""
        # Call API and return raw response
        pass
```

## Output Format

Each system returns a raw JSON response that is then parsed by the corresponding parser in `src/parsing/parsers.py`:

- **AWS Textract**: Returns `Blocks` with text and metadata
- **Azure Vision**: Returns `readResult.blocks` with lines and text
- **Azure Document**: Returns `pages` with lines and content
- **Google Vision**: Returns `fullTextAnnotation` with text
- **Google Document**: Returns `document` with text and page structure

## Usage

Systems are instantiated via the factory pattern in `src/ocr_systems/__init__.py`. Configuration is loaded from `config/experiments.yaml`.

Example:
```python
from src.ocr_systems import OCRSystemFactory

# Create system instance
system = OCRSystemFactory.create_system('aws_textract', config)

# Extract raw output
raw_output = system.extract_raw_output('path/to/image.jpg')
```

## Authentication

### AWS Textract
- Requires AWS credentials (access key ID and secret access key)
- Or uses AWS CLI default credentials

### Azure Services
- Requires endpoint URL and subscription key (credential)
- Each service has its own endpoint and key

### Google Services
- Requires service account JSON credentials
- Project ID and location/processor configuration

See `setup/[system]/README.md` for detailed setup instructions for each system.

