# Google Gemini Flash Setup

## Prerequisites

You need a Google AI Studio account with API access.

## Google AI Studio Setup

1. **Access Google AI Studio:**
   - Go to [Google AI Studio](https://aistudio.google.com)
   - Sign in with your Google account

2. **Get API Key:**
   - Navigate to "Get API key" in the left sidebar
   - Click "Create API key"
   - Copy and save the key securely

## Python Package Installation

```bash
pip install -r requirements.txt
```

## Configuration

Gemini Flash supports the following parameters in `config/experiments.yaml`:

- `api_key`: Google AI API key (required)
- `model`: Model name (default: `gemini-2.0-flash-exp`)
- `prompt`: Custom OCR prompt (optional)
- `max_tokens`: Maximum tokens in response (default: `8192`)
- `temperature`: Sampling temperature (default: `0.0` for deterministic output)
- `measure_time`: Measure processing time (default: `false`)

### Example Configuration

```yaml
ocr_systems:
  - name: "gemini_flash"
    type: "commercial_llm"
    config:
      api_key: "AIzaSy..."
      model: "gemini-2.0-flash-exp"
      prompt: "Extract all visible text from this document image. Return only the text"
      max_tokens: 8192
      temperature: 0.0
      measure_time: true
```

### Environment Variables (Alternative)

You can also set the API key via environment variable:

```bash
export GOOGLE_API_KEY="AIzaSy..."
```

Then reference it in config:
```yaml
config:
  api_key: "${GOOGLE_API_KEY}"
```

## API Limits and Pricing

- **Pricing** (Gemini 2.0 Flash):
  - Input: $0.075 per 1M tokens (< 128K context)
  - Output: $0.30 per 1M tokens (< 128K context)
  - Images: Included in token count
- **Rate limits**: 
  - Free tier: 15 requests per minute, 1,500 requests per day
  - Paid tier: Higher limits available
- Refer to [Google AI Pricing](https://ai.google.dev/pricing)

## Prompt

The default prompt is optimized for OCR:
```
Extract all visible text from this document image. Return only the text
```

## Reference

- Google AI Studio: https://aistudio.google.com
- Gemini API documentation: https://ai.google.dev/gemini-api/docs
- Pricing: https://ai.google.dev/pricing

