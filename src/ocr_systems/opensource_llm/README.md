# Open-source LLM OCR Systems

This directory contains implementations of open-source multimodal LLMs for OCR tasks, served via vLLM with OpenAI-compatible API.

## Implemented Systems

| System | Model Name | Parameters | HuggingFace Model ID |
|--------|------------|------------|----------------------|
| **Qwen 2.5 VL** | Qwen2.5-VL-3B-Instruct | 3B | `Qwen/Qwen2.5-VL-3B-Instruct` |
| **Gemma 3** | Gemma-3-2B-IT | 2B | `google/gemma-3-2b-it` | 

## Architecture

All open-source LLM systems use a **single generic class** (`VLLMOpenAIOCR`) that communicates with vLLM via OpenAI-compatible API. The model is specified in the configuration:

```python
class VLLMOpenAIOCR(OCRSystem):
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.api_url = config.get('api_url')
        self.hf_model_name = config.get('hf_model_name')  # Model specified in config
    
    def extract_raw_output(self, image_path: str) -> Dict[str, Any]:
        """Extract raw output via vLLM OpenAI-compatible API"""
        # 1. Convert image to base64 PNG
        # 2. Prepare OpenAI-compatible payload with hf_model_name
        # 3. POST to vLLM endpoint
        # 4. Return JSON response
        pass
```

## vLLM Server Setup

### Starting the Server

Before running experiments, start a vLLM server with the desired model:

```bash
# For Qwen 2.5 VL
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-VL-3B-Instruct \
    --port 8000 \
    --gpu-memory-utilization 0.9

# For Gemma 3
python -m vllm.entrypoints.openai.api_server \
    --model google/gemma-3-2b-it \
    --port 8000 \
    --gpu-memory-utilization 0.9
```

See `setup/opensource_llm/README.md` for detailed server setup and deployment scripts.

## API Communication

Systems communicate with vLLM using OpenAI-compatible format:

**Request:**
```json
{
  "model": "Qwen/Qwen2.5-VL-3B-Instruct",
  "messages": [
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "Extract all visible text..."},
        {"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}
      ]
    }
  ],
  "max_tokens": 1024,
  "temperature": 0.0
}
```

**Response:** Standard OpenAI chat completion format with `choices[].message.content`

## Output Format

All systems return responses in OpenAI-compatible format:
- **Structure**: `choices[].message.content` contains the extracted text
- **Parser**: Single shared parser `parse_vllm_openai` for all vLLM models


## Usage

Both `qwen25vl` and `gemma3` use the **same implementation class** (`VLLMOpenAIOCR`) registered under different names. The model is determined by the `hf_model_name` in the configuration.

**Important**: Ensure vLLM server is running before running experiments with these systems.

Example:
```python
from src.ocr_systems import OCRSystemFactory

# Both create VLLMOpenAIOCR instances with different configurations
qwen_system = OCRSystemFactory.create_system('qwen25vl', qwen_config)
gemma_system = OCRSystemFactory.create_system('gemma3', gemma_config)

# Extract raw output
raw_output = qwen_system.extract_raw_output('path/to/image.jpg')
```

**Adding New Models**: To add a new vLLM-compatible vision model, simply:
1. Register it in `src/ocr_systems/__init__.py` with `VLLMOpenAIOCR`
2. Add parser mapping in `src/parsing/parsers.py` to `parse_vllm_openai`
3. Add configuration in `config/experiments.yaml` with correct `hf_model_name`

## Deployment

For deployment scripts and examples, see:
- `setup/opensource_llm/README.md` - vLLM server setup
- Example deployment scripts (coming soon)

## Reference

- vLLM documentation: https://docs.vllm.ai
- Qwen 2.5 VL: https://huggingface.co/Qwen/Qwen2.5-VL-3B-Instruct
- Gemma 3: https://huggingface.co/google/gemma-3-2b-it

