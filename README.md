# OCR Systems Assessment

Repository for evaluating and comparing commercial and open-source OCR systems and multimodal LLMs on text recognition.

## Setup

This repository includes **14 OCR systems** across 4 categories:
- **3 Open-source OCR**: Tesseract, PaddleOCR, DocTR
- **5 Commercial OCR**: AWS Textract, Azure Vision, Azure Document Intelligence, Google Vision, Google Document AI
- **4 Commercial LLM**: GPT-4o, Gemini Flash, Claude Haiku, Mistral Document AI
- **2 Open-source LLM** (via vLLM with OpenAI-compatible API): Qwen 2.5 VL, Gemma 3

**Installation:**
```bash
# Install dependencies for a specific system
pip install -r setup/{system_name}/requirements.txt
```

See `setup/{system}/README.md` for detailed setup instructions, including:
- System-specific requirements
- Authentication and credentials setup
- Configuration parameters
- Pricing details (for commercial systems)

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
