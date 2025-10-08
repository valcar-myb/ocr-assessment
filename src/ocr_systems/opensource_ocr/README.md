# Open Source OCR Systems

This directory contains implementations of open-source OCR systems for the benchmark.

## Implemented Systems

| System | Framework/Library | Detection Model | Recognition Model | Language | Device |
|--------|-------------------|-----------------|-------------------|----------|--------|
| **Tesseract** | Tesseract OCR v5 | Built-in | LSTM (OEM 3) | English (`eng`) | CPU |
| **PaddleOCR** | PaddlePaddle | PP-OCRv5 Server Det | PP-OCRv5 Server Rec | English (`en`) | CPU |
| **DocTR** | Mindee DocTR | DB ResNet50 | CRNN VGG16-BN | Multilingual | CPU |

## Configuration Details

### Tesseract
- **Version**: Tesseract 5.x
- **Language**: `eng` (English)
- **PSM** (Page Segmentation Mode): `3` (Fully automatic page segmentation)
- **OEM** (OCR Engine Mode): `3` (Default, based on what is available - LSTM preferred)
- **Type**: Traditional OCR with LSTM neural network

### PaddleOCR
- **Framework**: PaddlePaddle
- **Detection Model**: `PP-OCRv5_server_det` (Server version for better accuracy)
- **Recognition Model**: `PP-OCRv5_server_rec` (Server version for better accuracy)
- **Language**: `en` (English)
- **Features**: Two-stage approach (detection + recognition)

### DocTR
- **Framework**: PyTorch-based
- **Detection Architecture**: `db_resnet50` (Differentiable Binarization with ResNet-50)
- **Recognition Architecture**: `crnn_vgg16_bn` (CRNN with VGG16-BN backbone)
- **Pretrained**: Yes (using pretrained weights)
- **Device**: CPU (configurable to GPU with CUDA)
- **Features**: End-to-end document understanding

## Architecture

All open-source OCR implementations follow the same pattern:

```python
class OpenSourceOCR(OCRSystem):
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        # Initialize model-specific parameters
        self._init_predictor()
    
    def _init_predictor(self):
        """Initialize the OCR model"""
        # Load and configure the model
        pass
    
    def extract_raw_output(self, image_path: str) -> Dict[str, Any]:
        """Extract raw output from the OCR system"""
        # Run OCR and return raw results
        pass
```

## Output Format

Each system returns a raw output that is then parsed by the corresponding parser in `src/parsing/parsers.py`:

- **Tesseract**: Returns `text` and `data` dictionary with word-level information
- **PaddleOCR**: Returns `rec_texts` array with detected text lines
- **DocTR**: Returns hierarchical structure with `pages`, `blocks`, `lines`, and `words`

## Model Characteristics

### Tesseract
- **Pros**: Mature, widely used, good for printed text
- **Cons**: Less accurate on complex layouts compared to deep learning methods
- **Best for**: Clean documents, printed text

### PaddleOCR
- **Pros**: High accuracy, multilingual support, active development
- **Cons**: Heavier than Tesseract, requires more resources
- **Best for**: General-purpose OCR, Asian languages

### DocTR
- **Pros**: Modern architecture, document-level understanding, PyTorch-based
- **Cons**: Requires more computational resources
- **Best for**: Document analysis, structured documents

## Usage

Systems are instantiated via the factory pattern in `src/ocr_systems/__init__.py`. Configuration is loaded from `config/experiments.yaml`.

Example:
```python
from src.ocr_systems import OCRSystemFactory

# Create system instance
system = OCRSystemFactory.create_system('tesseract', config)

# Extract raw output
raw_output = system.extract_raw_output('path/to/image.jpg')
```

## Installation

Each system requires specific dependencies. See `setup/[system]/README.md` for detailed installation instructions:

- **Tesseract**: Requires system-level installation + Python wrapper
- **PaddleOCR**: Python package via pip
- **DocTR**: Python package via pip (PyTorch-based)

