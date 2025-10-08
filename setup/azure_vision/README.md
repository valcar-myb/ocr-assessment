# Microsoft Azure AI Vision Setup

## Prerequisites

You need an Azure account with Azure AI Vision service enabled.

## Azure Setup

1. **Create Azure AI Vision Resource:**
   - Go to [Azure Portal](https://portal.azure.com)
   - Create a new "Computer Vision" or "Azure AI Vision" resource
   - Note your endpoint URL and API key

2. **Get Credentials:**
   - After creating the resource, go to "Keys and Endpoint"
   - Copy the endpoint URL (e.g., `https://your-resource.cognitiveservices.azure.com/`)
   - Copy one of the API keys

## Python Package Installation

```bash
pip install -r requirements.txt
```

## Configuration

Azure Vision supports the following parameters in `config/experiments.yaml`:

- `endpoint`: Azure Vision endpoint URL (required)
- `credential`: Azure Vision API key (required)
- `model_version`: Model version to use (default: `latest`)
- `measure_time`: Measure processing time (default: `false`)

### Example Configuration

```yaml
ocr_systems:
  - name: "azure_vision"
    type: "commercial_ocr"
    config:
      endpoint: "https://your-resource.cognitiveservices.azure.com/"
      credential: "your_api_key_here"
      model_version: "latest"
      measure_time: true
```

### Environment Variables (Alternative)

You can also set credentials via environment variables:

```bash
export AZURE_VISION_ENDPOINT="https://your-resource.cognitiveservices.azure.com/"
export AZURE_VISION_KEY="your_api_key_here"
```

Then reference them in config:
```yaml
config:
  endpoint: "${AZURE_VISION_ENDPOINT}"
  credential: "${AZURE_VISION_KEY}"
```

## Supported Regions

Azure AI Vision is available in multiple regions:
- `eastus` (US East)
- `westus` (US West)
- `westeurope` (West Europe)
- `southeastasia` (Southeast Asia)

Check [Azure documentation](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/) for full list.

## API Limits and Pricing

- **Rate limits**: Depends on your pricing tier (Free: 20 calls/min, Standard: varies)
- **Free tier**: 5,000 transactions per month
- **Pricing**: Pay per 1,000 transactions
- Refer to [Azure AI Vision pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/computer-vision/)

## Features

Azure Vision READ API provides:
- Text extraction from images
- Support for printed and handwritten text
- Multiple language support
- Layout analysis with bounding boxes
- Confidence scores for detected text

## Reference

- Azure AI Vision documentation: https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/
- Image Analysis SDK: https://learn.microsoft.com/en-us/azure/ai-services/computer-vision/quickstarts-sdk/image-analysis-client-library-40

