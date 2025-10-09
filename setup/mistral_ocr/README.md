# Mistral OCR Setup

## Prerequisites

You need a Mistral AI account with API access.

## Mistral AI Setup

1. **Create Mistral Account:**
   - Go to [Mistral AI Console](https://console.mistral.ai)
   - Sign up or log in

2. **Get API Key:**
   - Navigate to [API Keys](https://console.mistral.ai/api-keys/)
   - Click "Create new key"
   - Copy and save the key securely

## Python Package Installation

```bash
pip install -r requirements.txt
```

## Configuration

Mistral OCR supports the following parameters in `config/experiments.yaml`:

- `api_key`: Mistral AI API key (required)
- `model`: Model name (default: `pixtral-12b-2409`)
- `measure_time`: Measure processing time (default: `false`)

### Example Configuration

```yaml
ocr_systems:
  - name: "mistral_ocr"
    type: "commercial_llm"
    config:
      api_key: "..."
      model: "pixtral-12b-2409"
      measure_time: true
```

### Environment Variables (Alternative)

You can also set the API key via environment variable:

```bash
export MISTRAL_API_KEY="..."
```

Then reference it in config:
```yaml
config:
  api_key: "${MISTRAL_API_KEY}"
```

## API Limits and Pricing

- **Pricing** (Pixtral 12B):
  - Input: $0.15 per 1M tokens
  - Output: $0.15 per 1M tokens
- **Rate limits**: Vary by subscription tier
- Refer to [Mistral Pricing](https://mistral.ai/technology/#pricing)

## Output Format

Mistral OCR returns results in Markdown format, providing structured text extraction with layout information preserved.

## Reference

- Mistral Console: https://console.mistral.ai
- Mistral API documentation: https://docs.mistral.ai
- Pricing: https://mistral.ai/technology/#pricing

