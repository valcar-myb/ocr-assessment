# Commercial LLM OCR Systems

This directory contains implementations of commercial Large Language Model (LLM) systems with vision capabilities for OCR tasks.

## Implemented Systems

| System | Provider | Model | Pricing Type |
|--------|----------|-------|--------------|
| **GPT-4o** | OpenAI | `gpt-4o` | Token-based |
| **Gemini Flash** | Google AI | `gemini-2.0-flash` | Token-based |
| **Claude Haiku** | Anthropic | `claude-3-5-haiku-20241022` | Token-based |
| **Mistral OCR** | Mistral AI | `mistral-ocr-latest` | Page-based |


## Architecture

All commercial LLM implementations follow the same pattern:

```python
class CommercialLLMOCR(OCRSystem):
    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.model = None
        self._init_predictor()
    
    def _init_predictor(self):
        """Initialize the LLM API client"""
        # Setup authentication and client
        pass
    
    def extract_raw_output(self, image_path: str) -> Dict[str, Any]:
        """Extract raw output from the LLM vision API"""
        # Encode image and call API
        pass
```

## Output Format

Each system returns a raw output that is then parsed by the corresponding parser in `src/parsing/parsers.py`:

- **GPT-4o**: Returns `choices[].message.content` with extracted text
- **Gemini Flash**: Returns `candidates[].content.parts[].text` with extracted text
- **Claude Haiku**: Returns `content[].text` with extracted text
- **Mistral OCR**: Returns `pages[].markdown` with structured text in Markdown format

## Common Configuration

All systems support:
- `api_key`: Provider-specific API key (required)
- `model`: Model identifier (required)
- `measure_time`: Enable processing time measurement (optional)

Vision-based models (GPT-4o, Gemini, Claude) additionally support:
- `prompt`: Custom OCR instruction prompt
- `max_tokens`: Maximum tokens in response
- `temperature`: Sampling temperature (0.0 recommended for OCR)

## Usage

Systems are instantiated via the factory pattern in `src/ocr_systems/__init__.py`. Configuration is loaded from `config/experiments.yaml`.

Example:
```python
from src.ocr_systems import OCRSystemFactory

# Create system instance
system = OCRSystemFactory.create_system('gpt4o', config)

# Extract raw output
raw_output = system.extract_raw_output('path/to/image.jpg')
```



## Authentication

All systems require API keys:
- **OpenAI**: Get from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Google AI**: Get from [Google AI Studio](https://aistudio.google.com)
- **Anthropic**: Get from [Anthropic Console](https://console.anthropic.com/settings/keys)
- **Mistral AI**: Get from [Mistral Console](https://console.mistral.ai/api-keys/)

See `setup/[system]/README.md` for detailed setup instructions for each system.

