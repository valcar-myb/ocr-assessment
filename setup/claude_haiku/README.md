# Anthropic Claude Haiku Setup

## Prerequisites

You need an Anthropic account with API access and credits.

## Anthropic Setup

1. **Create Anthropic Account:**
   - Go to [Anthropic Console](https://console.anthropic.com)
   - Sign up or log in

2. **Get API Key:**
   - Navigate to [API Keys](https://console.anthropic.com/settings/keys)
   - Click "Create Key"
   - Copy and save the key securely

3. **Add Credits:**
   - Ensure you have credits in your account
   - Claude requires paid credits

## Python Package Installation

```bash
pip install -r requirements.txt
```

## Configuration

Claude Haiku supports the following parameters in `config/experiments.yaml`:

- `api_key`: Anthropic API key (required)
- `model`: Model name (default: `claude-3-5-haiku-20241022`)
- `prompt`: Custom OCR prompt (optional)
- `max_tokens`: Maximum tokens in response (default: `4096`)
- `temperature`: Sampling temperature (default: `0.0` for deterministic output)
- `measure_time`: Measure processing time (default: `false`)

### Example Configuration

```yaml
ocr_systems:
  - name: "claude_haiku"
    type: "commercial_llm"
    config:
      api_key: "sk-ant-..."
      model: "claude-3-5-haiku-20241022"
      prompt: "Extract all visible text from this document image. Return only the text"
      max_tokens: 4096
      temperature: 0.0
      measure_time: true
```

### Environment Variables (Alternative)

You can also set the API key via environment variable:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

Then reference it in config:
```yaml
config:
  api_key: "${ANTHROPIC_API_KEY}"
```

## API Limits and Pricing

- **Pricing** (Claude 3.5 Haiku):
  - Input: $0.80 per MTok (million tokens)
  - Output: $4.00 per MTok
  - Images: Counted as tokens based on size
- **Rate limits**: Vary by tier, check [Anthropic documentation](https://docs.anthropic.com/en/api/rate-limits)
- Refer to [Anthropic Pricing](https://www.anthropic.com/pricing)

## Prompt

```
Extract all visible text from this document image. Return only the text.
```

## Reference

- Anthropic Console: https://console.anthropic.com
- Claude API documentation: https://docs.anthropic.com
- Pricing: https://www.anthropic.com/pricing

