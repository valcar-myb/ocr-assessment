## OCR Evaluation Datasets

This directory contains instructions for preparing datasets for OCR system assessment.

### Dataset Setup Instructions

1. **Images**: Place your test images (`.jpg` or `.png`) in `raw/sample_dataset/images/`
2. **Ground Truth**: Create corresponding `.txt` files with the same filename in `raw/sample_dataset/ground_truth/`
3. **Metadata**: Create a `dataset.json` file in `raw/sample_dataset/` with the following structure:

```json
[
  {
    "img": "images/image001.jpg",
    "gt": "ground_truth/image001.txt"
  },
  {
    "img": "images/image002.png", 
    "gt": "ground_truth/image002.txt"
  }
]
```

### Directory Structure
```
data/
├── raw/
│   └── sample_dataset/
│       ├── images/
│       ├── ground_truth/
│       └── dataset.json
└── README.md
```

### File Formats
- Images: `.jpg`, `.png` files
- Ground Truth: `.txt` files with plain text content
- Metadata: `dataset.json` with image-ground truth mappings

### Usage
The evaluation system will automatically load datasets from this directory based on the configuration in `config/experiments.yaml`.
