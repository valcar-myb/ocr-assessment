# OCR Systems Assessment

Repository for evaluating and comparing modern OCR systems in the era of LLMs.

## Setup

Install OCR systems (choose based on what you need):

```bash
# DocTR
pip install -r setup/doctr/requirements.txt

# PaddleOCR
pip install -r setup/paddleocr/requirements.txt

# Tesseract (see setup/tesseract/README.md for system installation)
pip install -r setup/tesseract/requirements.txt
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
  - `ocr_systems/`: OCR system implementations (DocTR, PaddleOCR, Tesseract)
  - `parsing/`: Parsers for raw OCR outputs
  - `evaluation/`: Evaluation metrics
- `data/`: Dataset directory
- `experiments/`: Pipeline scripts
- `results/`: Generated outputs (not tracked)
