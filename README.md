# OCR Systems Assessment

Repository for evaluating and comparing modern OCR systems in the era of LLMs.

## Setup

1. Install core dependencies:
```bash
pip install -r requirements.txt
```

2. Install specific system requirements (choose based on systems you want to evaluate):
```bash
# Open-source OCR engines
pip install -r requirements/opensource_ocr.txt

# Commercial OCR services  
pip install -r requirements/commercial_ocr.txt

# Open-source multimodal LLMs
pip install -r requirements/opensource_llm.txt

# Commercial multimodal LLMs
pip install -r requirements/commercial_llm.txt
```

3. Download datasets (see `data/README.md`)

4. Configure experiment in `config/experiments.yaml`

5. Run assessment:
```bash
python experiments/run_assessment.py
```

## Structure

- `config/`: Experiment configuration files
- `src/`: Source code modules organized by system type
  - `ocr_systems/`: OCR system implementations
    - `opensource_ocr/`: Tesseract, PaddleOCR, EasyOCR, DocTR
    - `commercial_ocr/`: Azure, Google, AWS services
    - `opensource_llm/`: Gemma 3, Qwen2.5-VL
    - `commercial_llm/`: GPT-4o, Gemini, Claude, MistralOCR
  - `evaluation/`: Evaluation metrics and framework
  - `utils/`: Utility functions
- `data/`: Dataset directory with download instructions
- `experiments/`: Main experiment scripts
- `results/`: Output metrics and results
- `notebooks/`: Analysis notebooks
- `requirements/`: Separate dependency files for each system category
