# OCR Systems Assessment

Repository for evaluating and comparing modern OCR systems in the era of LLMs.

## Setup

Install OCR systems (choose based on what you need):

```bash
# Open-source OCR systems
# DocTR
pip install -r setup/doctr/requirements.txt

# PaddleOCR
pip install -r setup/paddleocr/requirements.txt

# Tesseract (see setup/tesseract/README.md for system installation)
pip install -r setup/tesseract/requirements.txt

# Commercial OCR systems
# AWS Textract (requires AWS account and credentials)
pip install -r setup/aws_textract/requirements.txt

# Azure AI Vision (requires Azure account and credentials)
pip install -r setup/azure_vision/requirements.txt

# Azure Document Intelligence (requires Azure account and credentials)
pip install -r setup/azure_document/requirements.txt

# Google Cloud Vision (requires GCP account and credentials)
pip install -r setup/google_vision/requirements.txt

# Google Cloud Document AI (requires GCP account and credentials)
pip install -r setup/google_document/requirements.txt

# Commercial LLM systems
# OpenAI GPT-4o (requires OpenAI API key and credits)
pip install -r setup/gpt4o/requirements.txt

# Google Gemini Flash (requires Google AI API key)
pip install -r setup/gemini_flash/requirements.txt

# Anthropic Claude Haiku (requires Anthropic API key and credits)
pip install -r setup/claude_haiku/requirements.txt

# Mistral OCR (requires Mistral AI API key)
pip install -r setup/mistral_ocr/requirements.txt
```

See `setup/{system}/README.md` for detailed installation instructions.

## Usage

### 1. Prepare datasets
See `data/README.md` for dataset preparation instructions.

### 2. Configure experiment
Edit `config/experiments.yaml` to select datasets, OCR systems, and metrics.

### 3. Run OCR extraction
```bash
python experiments/run_pipeline.py --step extract
```

### 4. Generate text files
```bash
python experiments/generate_text.py
```

### 5. Run evaluation
```bash
python experiments/run_pipeline.py --step evaluate
```

## Structure

- `setup/`: Installation instructions and requirements per OCR system
- `src/`: Source code
  - `ocr_systems/`: OCR system implementations
    - `opensource_ocr/`: Open-source systems (DocTR, PaddleOCR, Tesseract)
    - `commercial_ocr/`: Commercial systems (AWS Textract, Azure, Google)
    - `opensource_llm/`: Open-source LLM systems
    - `commercial_llm/`: Commercial LLM systems
  - `parsing/`: Parsers for raw OCR outputs
  - `evaluation/`: Evaluation metrics
- `data/`: Dataset directory
- `experiments/`: Pipeline scripts
- `results/`: Generated outputs (not tracked)
