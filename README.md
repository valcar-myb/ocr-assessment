# OCR Systems Assessment

Repository for evaluating and comparing commercial and open-source OCR systems and multimodal LLMs on text recognition.

## Quick Start
```bash
# Activate virtual environment
source venv/bin/activate

# Run complete evaluation pipeline
python run_experiments.py all

# Or run individual steps
python run_experiments.py extract    # Extract OCR text
python run_experiments.py evaluate   # Evaluate accuracy
python run_experiments.py summary    # Generate benchmark
```

### Available Commands
```bash
python run_experiments.py help         # Show all available commands
python run_experiments.py all          # Complete pipeline
python run_experiments.py extract      # OCR extraction only
python run_experiments.py generate_text # Generate cleaned text files
python run_experiments.py evaluate     # Accuracy evaluation only
python run_experiments.py summary      # Benchmark generation only
python run_experiments.py benchmark    # Generate benchmark from existing results
```

## Text Cleaning

The system includes **automatic text cleaning** for evaluation to ensure fair comparison between OCR systems:

- **Whitelist-based filtering** - Only keeps allowed characters (letters, digits, punctuation, whitespace)
- **Configurable character sets** - Customize allowed characters in `config/experiments_active.yaml`
- **Automatic application** - Applied during text file generation for evaluation
- **Statistics reporting** - Shows how many characters were removed during cleaning

**Example:**
```
Text cleaning enabled with whitelist: 26 uppercase + 26 lowercase + 10 digits + 19 punctuation
Cleaned text: 1072 -> 1023 characters
```

## Setup

This repository includes **14 OCR systems** across 4 categories:
- **3 Open-source OCR**: Tesseract, PaddleOCR, DocTR
- **5 Commercial OCR**: AWS Textract, Azure Vision, Azure Document Intelligence, Google Vision, Google Document AI
- **4 Commercial LLM**: GPT-4o, Gemini Flash, Claude Haiku, Mistral Document AI
- **3 Open-source LLM** (via vLLM with OpenAI-compatible API): Qwen 2.5 VL, Gemma 3

### OCR System Installation

**Installation:**
```bash
# Install dependencies for a specific system
pip install -r setup/{system_name}/requirements.txt
```

**Note**: Open-source LLMs require a running vLLM server. See `setup/opensource_llm/README.md` for server setup.

See `setup/{system}/README.md` for detailed setup instructions, including:
- System-specific requirements
- Authentication and credentials setup (for commercial systems)
- vLLM server configuration (for open-source LLMs)
- Configuration parameters
- Pricing details (for commercial systems)

### Evaluation Tools

For accurate OCR evaluation, install [ocreval](https://github.com/eddieantonio/ocreval):

```bash
# macOS
brew install eddieantonio/eddieantonio/ocreval

# Linux - use provided installation script
bash setup/ocreval/install.sh
```

See `setup/ocreval/README.md` for detailed installation instructions and troubleshooting.

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

Evaluation uses [ocreval](https://github.com/eddieantonio/ocreval) with a two-phase workflow:

#### Option A: Use the pipeline (recommended)
```bash
# Run full evaluation pipeline
python run_experiments.py evaluate

# Generate benchmark summary
python run_experiments.py summary

# Or run all steps
python run_experiments.py all
```

#### Option B: Manual step-by-step
```bash
# Phase 1: Generate partial reports for each file
python experiments/evaluation/generate_partial_reports.py        # Character (accuracy)
python experiments/evaluation/generate_word_partial_reports.py   # Word (wordacc)

# Phase 2: Aggregate reports
python experiments/aggregation/aggregate_reports.py               # Character (accsum)
python experiments/aggregation/aggregate_word_reports.py          # Word (wordaccsum)
python experiments/aggregation/aggregate_all_reports.py           # Both

# Phase 3: Build benchmark from aggregated reports
python experiments/aggregation/build_benchmark.py
```

Results are saved to:
- Partial reports: `results/metrics/accuracy_reports/partials/` and `partials_word/`
- Aggregated reports: `results/metrics/accuracy_reports/aggregates/`
- Final benchmark: `results/benchmark/benchmark_data_latest.json` and `.csv`

## Structure

- `setup/`: Installation instructions and requirements per OCR system
  - `ocreval/`: Installation guide for ISRI OCR evaluation tools
- `src/`: Source code
  - `ocr_systems/`: OCR system implementations
    - `opensource_ocr/`: Open-source systems (DocTR, PaddleOCR, Tesseract)
    - `commercial_ocr/`: Commercial systems (AWS Textract, Azure, Google)
    - `opensource_llm/`: Open-source LLM systems
    - `commercial_llm/`: Commercial LLM systems
  - `parsing/`: Parsers for raw OCR outputs
  - `evaluation/`: Evaluation metrics
    - `accuracy/`: Accuracy evaluation (integrates ocreval)
    - `time/`: Time performance evaluation
    - `cost/`: Cost analysis
- `data/`: Dataset directory
- `experiments/`: Pipeline scripts
- `results/`: Generated outputs (not tracked)
