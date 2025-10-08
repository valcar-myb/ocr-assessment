# OCR Pipeline Usage

## Overview

The OCR evaluation pipeline is modular and allows running specific steps independently.

## Pipeline Steps

### Step 1: OCR Text Extraction (`--step extract`)
- Runs OCR systems on all images in the dataset
- Generates raw text outputs for each system
- Saves results to `results/raw_outputs/`
- Format: `{dataset}_{system}_raw.json`

### Step 2: Evaluation (`--step evaluate`)
- Calculates metrics on the raw OCR outputs
- Compares predictions with ground truth
- Generates evaluation results for each system
- Saves results to `results/metrics/`
- Format: `{dataset}_{system}_eval.json`

### Step 3: Summary Report (`--step summary`)
- Aggregates all evaluation results
- Creates a comprehensive summary report
- Saves to `results/metrics/summary_report.json`

## Usage Examples

```bash
# Run all steps
python experiments/run_pipeline.py

# Run only OCR extraction
python experiments/run_pipeline.py --step extract

# Run only evaluation (requires raw outputs)
python experiments/run_pipeline.py --step evaluate

# Run only summary generation
python experiments/run_pipeline.py --step summary

# Use custom config
python experiments/run_pipeline.py --config my_config.yaml --step extract
```

## Output Structure

```
results/
├── raw_outputs/
│   ├── sroie_doctr_raw.json
│   └── sroie_tesseract_raw.json
└── metrics/
    ├── sroie_doctr_eval.json
    ├── sroie_tesseract_eval.json
    └── summary_report.json
```

