# Experiments Directory Structure

This directory contains all the experimental scripts and tools for the OCR evaluation pipeline, organized by functionality.

## Directory Structure

### 📁 `core/`
Main pipeline and orchestration scripts:
- `run_pipeline.py` - Main pipeline orchestrator that runs the complete OCR evaluation workflow

### 📁 `evaluation/`
Scripts for evaluating OCR accuracy and generating reports:
- `evaluate_accuracy.py` - Main accuracy evaluation script
- `generate_partial_reports.py` - Generates individual accuracy reports for each image
- `generate_word_partial_reports.py` - Generates word-level accuracy reports

### 📁 `aggregation/`
Scripts for aggregating and summarizing evaluation results:
- `aggregate_all_reports.py` - Aggregates all evaluation reports
- `aggregate_reports.py` - Aggregates character-level accuracy reports
- `aggregate_word_reports.py` - Aggregates word-level accuracy reports
- `build_benchmark.py` - Builds final benchmark summary with metrics

### 📁 `utilities/`
Utility scripts for data processing and validation:
- `generate_text.py` - Text generation utilities
- `verify_utf8.py` - UTF-8 encoding verification tool

## Usage

### Running the Complete Pipeline
```bash
python experiments/core/run_pipeline.py --config config/experiments_active.yaml --step all
```

### Running Individual Steps
```bash
# Extract OCR text
python experiments/core/run_pipeline.py --config config/experiments_active.yaml --step extract

# Evaluate accuracy
python experiments/core/run_pipeline.py --config config/experiments_active.yaml --step evaluate

# Generate summary
python experiments/core/run_pipeline.py --config config/experiments_active.yaml --step summary
```

### Running Individual Components
```bash
# Generate partial reports
python experiments/evaluation/generate_partial_reports.py

# Aggregate reports
python experiments/aggregation/aggregate_reports.py

# Build benchmark
python experiments/aggregation/build_benchmark.py
```

## Configuration

The pipeline uses configuration files in the `config/` directory:
- `experiments_active.yaml` - Active configuration with enabled systems
- `experiments.yaml` - Complete configuration with all available systems (commented)

## Output Structure

Results are saved in the `results/` directory:
- `results/raw_outputs/` - Raw OCR outputs from each system
- `results/text_outputs/` - Processed text outputs
- `results/metrics/` - Accuracy evaluation results
- `results/benchmark/` - Final benchmark summaries