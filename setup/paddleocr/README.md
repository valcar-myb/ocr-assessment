# PaddleOCR Setup

## Installation

```bash
pip install -r requirements.txt
```

## System Requirements

- Python >= 3.8
- PaddlePaddle >= 2.5.0

## Configuration

PaddleOCR supports the following parameters in `config/experiments.yaml`:

- `det_model`: Detection model name (default: `PP-OCRv3`)
- `rec_model`: Recognition model name (default: `PP-OCRv3`)
- `lang`: Language code (default: `en`)
- `measure_time`: Measure processing time (default: `false`)

## Available Models

### Detection Models:
- `PP-OCRv3` - Lightweight PP-OCRv3 detector
- `PP-OCRv4` - Latest PP-OCRv4 detector
- `PP-OCRv5_server_det` - Server version with higher accuracy

### Recognition Models:
- `PP-OCRv3` - Lightweight PP-OCRv3 recognizer
- `PP-OCRv4` - Latest PP-OCRv4 recognizer
- `PP-OCRv5_server_rec` - Server version with higher accuracy

## Reference

PaddleOCR documentation: https://github.com/PaddlePaddle/PaddleOCR
