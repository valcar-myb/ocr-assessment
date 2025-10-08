# Tesseract OCR Setup

## System Installation

Tesseract requires system-level installation:

### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-eng  # English language data
```

### macOS:
```bash
brew install tesseract
```

### Windows:
Download installer from: https://github.com/UB-Mannheim/tesseract/wiki

## Python Package Installation

```bash
pip install -r requirements.txt
```

## Configuration

Tesseract supports the following parameters in `config/experiments.yaml`:

- `language`: Language code (default: `eng`)
- `psm`: Page segmentation mode (default: `3`)
- `oem`: OCR Engine mode (default: `3`)
- `measure_time`: Measure processing time (default: `false`)

## Page Segmentation Modes (PSM)

- `0`: Orientation and script detection only
- `1`: Automatic page segmentation with OSD
- `3`: Fully automatic page segmentation, but no OSD (default)
- `6`: Assume a single uniform block of text
- `11`: Sparse text. Find as much text as possible

## OCR Engine Modes (OEM)

- `0`: Legacy engine only
- `1`: Neural nets LSTM engine only
- `2`: Legacy + LSTM engines
- `3`: Default, based on what is available (recommended)

## Reference

Tesseract documentation: https://github.com/tesseract-ocr/tesseract
