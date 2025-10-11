# Accuracy Evaluation Module

This module provides tools to evaluate OCR system accuracy using various metrics.

## Integration with ocreval

This module integrates [ocreval](https://github.com/eddieantonio/ocreval), a modern port of the ISRI Analytic Tools for OCR Evaluation with UTF-8 support. The `ocreval` toolkit provides industry-standard metrics for OCR evaluation and is used for accurate character and word accuracy calculations.

**Installation**: See `setup/ocreval/README.md` for installation instructions.

**Citation**: Santos, E. A. (2019). OCR evaluation tools for the 21st century. In *Proceedings of the 3rd Workshop on the Use of Computational Methods in the Study of Endangered Languages* (pp. 23-27). https://www.aclweb.org/anthology/W19-6004/

## Metrics

The following metrics are implemented:

### 1. Character Error Rate (CER)
- Measures character-level errors (insertions, deletions, substitutions)
- Formula: `CER = Levenshtein Distance / Total Characters`
- Range: [0, ∞) where 0 = perfect, higher = worse

### 2. Word Error Rate (WER)
- Measures word-level errors (insertions, deletions, substitutions)
- Formula: `WER = Word Levenshtein Distance / Total Words`
- Range: [0, ∞) where 0 = perfect, higher = worse

### 3. Character Accuracy
- Percentage of correctly recognized characters
- Range: [0, 1] where 1 = perfect, 0 = completely wrong

### 4. Word Accuracy
- Percentage of correctly recognized words
- Range: [0, 1] where 1 = perfect, 0 = completely wrong

### 5. Normalized Edit Distance (NED)
- Levenshtein distance normalized by text length
- Range: [0, 1] where 0 = perfect, 1 = completely different

## Usage

### Evaluate a single OCR tool

```python
from pathlib import Path
from evaluation.accuracy import AccuracyEvaluator

# Initialize evaluator (uses ocreval)
evaluator = AccuracyEvaluator(save_detailed_reports=True)

results = evaluator.evaluate_dataset(
    dataset_name='sroie',
    ocr_tool_name='tesseract',
    text_outputs_dir=Path('results/text_outputs/sroie/tesseract'),
    ground_truth_dir=Path('data/raw/sroie/gt'),
    dataset_json=Path('data/raw/sroie/dataset.json')
)

print(results)
```

### Evaluate all OCR tools on a dataset

```python
from pathlib import Path
from evaluation.accuracy import AccuracyEvaluator

# Initialize evaluator
# save_detailed_reports=True will save per-file reports in results/metrics/accuracy_reports/
evaluator = AccuracyEvaluator(save_detailed_reports=True)

results = evaluator.evaluate_all_tools(
    dataset_name='sroie',
    dataset_json=Path('data/raw/sroie/dataset.json'),
    ground_truth_dir=Path('data/raw/sroie/gt'),
    text_outputs_base_dir=Path('results/text_outputs/sroie')
)

# Save results
evaluator.save_results(results, Path('results/metrics/sroie_accuracy.json'))

# Print summary
evaluator.print_summary(results)
```

### Using ocreval directly

```python
from pathlib import Path
from evaluation.accuracy import OCREvalWrapper

# Initialize ocreval wrapper
ocreval = OCREvalWrapper()

# Run on single file pair
metrics = ocreval.run_accuracy(
    gt_path=Path('data/raw/sroie/gt/X00016469670.txt'),
    pred_path=Path('results/text_outputs/sroie/tesseract/X00016469670.txt'),
    output_path=Path('report.txt')  # Optional detailed report
)

print(f"Character Accuracy: {metrics['char_accuracy']:.4f}")
print(f"Word Accuracy: {metrics['word_accuracy']:.4f}")
```

### Calculate individual metrics

```python
from evaluation.accuracy import (
    calculate_cer,
    calculate_wer,
    calculate_character_accuracy
)

prediction = "Hello world"
ground_truth = "Hello World"

cer = calculate_cer(prediction, ground_truth)
wer = calculate_wer(prediction, ground_truth)
char_acc = calculate_character_accuracy(prediction, ground_truth)

print(f"CER: {cer:.4f}")
print(f"WER: {wer:.4f}")
print(f"Char Accuracy: {char_acc:.4f}")
```

## Testing ocreval Integration

Before running evaluations, test that ocreval is properly installed:

```bash
cd src/evaluation/accuracy
python test_ocreval.py
```

This will:
1. Check if ocreval is installed and accessible
2. Run a sample accuracy test on available data
3. Display metrics to verify everything works

## Running the Evaluation

The evaluation follows a **two-phase workflow**:

### Phase 1: Generate Partial Reports

#### Character Accuracy Partial Reports (accuracy)
Generate individual character accuracy reports for each file:

```bash
cd experiments
python generate_partial_reports.py
```

This will:
1. Run `accuracy` command for each (ground_truth, prediction) file pair
2. Save partial reports to `results/metrics/accuracy_reports/partials/{dataset}/{tool}/`
3. Each file gets its own `.txt` report

#### Word Accuracy Partial Reports (wordacc)
Generate individual word accuracy reports for each file:

```bash
cd experiments
python generate_word_partial_reports.py
```

This will:
1. Run `wordacc` command for each (ground_truth, prediction) file pair
2. Save partial word reports to `results/metrics/accuracy_reports/partials_word/{dataset}/{tool}/`
3. Each file gets its own `.txt` report

### Phase 2: Aggregate Reports

Aggregate all partial reports into summary reports:

#### Character Accuracy (accsum)
```bash
cd experiments
python aggregate_reports.py
```

This will:
1. Run `accsum` command on all partial reports for each tool
2. Save aggregated reports to `results/metrics/accuracy_reports/aggregates/{dataset}/`
3. Create files like `{dataset}_{tool}.txt`

#### Word Accuracy (wordaccsum)
```bash
cd experiments
python aggregate_word_reports.py
```

This will:
1. Run `wordaccsum` command on all partial reports for each tool
2. Save word accuracy aggregated reports to `results/metrics/accuracy_reports/aggregates/{dataset}/`
3. Create files like `{dataset}_{tool}_word.txt`

#### Both Character and Word Accuracy
```bash
cd experiments
python aggregate_all_reports.py
```

This runs both `accsum` and `wordaccsum` to generate both types of reports.

### All-in-One Evaluation

To run both phases and get JSON results:

```bash
cd experiments
python evaluate_accuracy.py
```

This will:
1. Generate partial reports (Phase 1)
2. Aggregate reports (Phase 2)
3. Parse aggregated reports
4. Save results to `results/metrics/sroie_accuracy.json`
5. Print a summary to console

## Output Format

The evaluation results are saved as JSON with the following structure:

```json
{
  "tesseract": {
    "dataset": "sroie",
    "ocr_tool": "tesseract",
    "n_samples": 10,
    "metrics": {
      "char_accuracy": 0.9477,
      "word_accuracy": 0.8766,
      "cer": 0.0523,
      "wer": 0.1234,
      "ned": 0.0523
    },
    "totals": {
      "total_chars": 12345,
      "total_words": 2456,
      "char_errors": 645,
      "word_errors": 303
    },
    "files_processed": ["X00016469670", ...]
  },
  "gpt4o": {
    ...
  }
}
```

### Report Structure

The evaluation generates two types of reports:

#### Partial Reports

**Character Accuracy (from `accuracy` command)**:
```
results/metrics/accuracy_reports/partials/{dataset}/{tool}/{file_id}.txt
```

**Word Accuracy (from `wordacc` command)**:
```
results/metrics/accuracy_reports/partials_word/{dataset}/{tool}/{file_id}.txt
```

Each partial report contains detailed analysis for a single file.

#### Aggregated Reports  
Summary reports for each tool on a dataset, saved to:

**Character Accuracy (accsum)**:
```
results/metrics/accuracy_reports/aggregates/{dataset}/{dataset}_{tool}.txt
```

**Word Accuracy (wordaccsum)**:
```
results/metrics/accuracy_reports/aggregates/{dataset}/{dataset}_{tool}_word.txt
```

Each aggregated report contains overall statistics across all files.

## Dependencies

### Python Dependencies
- `python-Levenshtein`: For efficient edit distance calculation
- Standard library: `json`, `pathlib`, `typing`

### External Tools
- **ocreval**: ISRI Analytic Tools for OCR Evaluation with UTF-8 support
  - Repository: https://github.com/eddieantonio/ocreval
  - Installation: See `setup/ocreval/README.md`
  - Commands used:
    - `accuracy`: Generate per-file character accuracy partial reports
    - `wordacc`: Generate per-file word accuracy partial reports
    - `accsum`: Aggregate character accuracy partial reports
    - `wordaccsum`: Aggregate word accuracy partial reports

