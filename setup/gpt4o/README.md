# OpenAI GPT-4o Vision Setup

## Prerequisites

You need an OpenAI account with API access and credits.

## OpenAI Setup

1. **Create OpenAI Account:**
   - Go to [OpenAI Platform](https://platform.openai.com)
   - Sign up or log in

2. **Get API Key:**
   - Navigate to [API Keys](https://platform.openai.com/api-keys)
   - Click "Create new secret key"
   - Copy and save the key securely

3. **Add Credits:**
   - Ensure you have credits in your account
   - GPT-4o Vision requires paid credits

## Python Package Installation

```bash
pip install -r requirements.txt
```

## Configuration

GPT-4o Vision supports the following parameters in `config/experiments.yaml`:

- `api_key`: OpenAI API key (required)
- `model`: Model name (default: `gpt-4o`)
- `prompt`: Custom OCR prompt (optional)
- `max_tokens`: Maximum tokens in response (default: `4096`)
- `temperature`: Sampling temperature (default: `0.0` for deterministic output)
- `measure_time`: Measure processing time (default: `false`)

### Example Configuration

```yaml
ocr_systems:
  - name: "gpt4o"
    type: "commercial_llm"
    config:
      api_key: "sk-..."
      model: "gpt-4o"
      prompt: "Extract all visible text from this document image. Return only the text"
      max_tokens: 4096
      temperature: 0.0
      measure_time: true
```

### Environment Variables (Alternative)

You can also set the API key via environment variable:

```bash
export OPENAI_API_KEY="sk-..."
```

Then reference it in config:
```yaml
config:
  api_key: "${OPENAI_API_KEY}"
```

## API Limits and Pricing

- **Pricing** (GPT-4o):
  - Input: $2.50 per 1M tokens
  - Output: $10.00 per 1M tokens
  - Images: Priced based on size (typically ~$0.00765 per image)
- Refer to [OpenAI Pricing](https://openai.com/api/pricing/)

## Prompt

The default prompt is optimized for OCR:
```
Extract all visible text from this document image. Return only the text
```

## Reference

- OpenAI API documentation: https://platform.openai.com/docs
- GPT-4o with Vision: https://platform.openai.com/docs/guides/vision
- Pricing: https://openai.com/api/pricing/

