# Mistral Document AI Setup

## Prerequisites

You need a Mistral AI account with Document AI access.

## Mistral AI Setup

1. **Create Mistral Account:**
   - Go to [La Plateforme](https://console.mistral.ai)
   - Sign up or log in

2. **Get API Key:**
   - Navigate to [API Keys](https://console.mistral.ai/api-keys/)
   - Click "Create new key"
   - Copy and save the key securely

3. **Enable Document AI:**
   - Ensure Document AI is enabled in your account
   - Check [Mistral Document AI](https://mistral.ai/solutions/document-ai) for features

## Python Package Installation

```bash
pip install -r requirements.txt
```

## Configuration

Mistral OCR supports the following parameters in `config/experiments.yaml`:

- `api_key`: Mistral AI API key (required)
- `model`: Model name (default: `mistral-ocr-latest`)
- `measure_time`: Measure processing time (default: `false`)

### Example Configuration

```yaml
ocr_systems:
  - name: "mistral_ocr"
    type: "commercial_llm"
    config:
      api_key: "..."
      model: "mistral-ocr-latest"
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

- **Pricing Model**: Page-based pricing for Document AI
- **Performance**: Up to 2,000 pages per minute on a single node
- **Accuracy**: 99%+ accuracy across global languages
- **Rate Limits**: Vary by subscription tier
- **Pricing Details**: Contact Mistral AI for Document AI pricing (differs from standard API token-based pricing)
- Refer to:
  - [Mistral Document AI](https://mistral.ai/solutions/document-ai)
  - [Mistral API Pricing](https://mistral.ai/pricing#api-pricing) (for reference on standard models)

## Features

Mistral Document AI provides:
- State-of-the-art OCR with 99%+ accuracy
- Multilingual support (11+ languages)
- Markdown-formatted output with layout preservation
- Table, form, and complex layout understanding
- Handwriting recognition
- Fast processing (2,000 pages/min on single GPU)
- Structured JSON output with custom templates

## Output Format

Mistral OCR returns results in **Markdown format**, providing structured text extraction with layout information preserved. This makes it ideal for document understanding tasks.

## Reference

- Mistral Console: https://console.mistral.ai
- Mistral Document AI: https://mistral.ai/solutions/document-ai
- API documentation: https://docs.mistral.ai


