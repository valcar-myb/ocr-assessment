# Microsoft Azure Document Intelligence Setup

## Prerequisites

You need an Azure account with Azure Document Intelligence (formerly Form Recognizer) service enabled.

## Azure Setup

1. **Create Azure Document Intelligence Resource:**
   - Go to [Azure Portal](https://portal.azure.com)
   - Create a new "Document Intelligence" or "Form Recognizer" resource
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

Azure Document Intelligence supports the following parameters in `config/experiments.yaml`:

- `endpoint`: Azure Document Intelligence endpoint URL (required)
- `credential`: Azure Document Intelligence API key (required)
- `model_id`: Model to use (default: `prebuilt-read`)
- `measure_time`: Measure processing time (default: `false`)

### Example Configuration

```yaml
ocr_systems:
  - name: "azure_document"
    type: "commercial_ocr"
    config:
      endpoint: "https://your-resource.cognitiveservices.azure.com/"
      credential: "your_api_key_here"
      model_id: "prebuilt-read"
      measure_time: true
```

### Available Models

Azure Document Intelligence supports multiple prebuilt models:
- `prebuilt-read`: General OCR for text extraction (recommended)
- `prebuilt-layout`: Layout analysis with tables and structure
- `prebuilt-invoice`: Invoice-specific extraction
- `prebuilt-receipt`: Receipt-specific extraction
- `prebuilt-idDocument`: ID document extraction

For this OCR benchmark, use `prebuilt-read`.

### Environment Variables (Alternative)

You can also set credentials via environment variables:

```bash
export AZURE_DOCUMENT_ENDPOINT="https://your-resource.cognitiveservices.azure.com/"
export AZURE_DOCUMENT_KEY="your_api_key_here"
```

## Supported Regions

Azure Document Intelligence is available in multiple regions:
- `eastus` (US East)
- `westus2` (US West 2)
- `westeurope` (West Europe)
- `southeastasia` (Southeast Asia)

Check [Azure documentation](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/) for full list.

## API Limits and Pricing

- **Rate limits**: 
  - Free tier: 500 pages per month, 1 call per minute
  - Standard tier: 15 transactions per second
- **Free tier**: 500 pages per month
- **Pricing**: Pay per page processed
- Refer to [Azure Document Intelligence pricing](https://azure.microsoft.com/en-us/pricing/details/ai-document-intelligence/)

## Features

Azure Document Intelligence READ model provides:
- High-quality text extraction
- Support for printed and handwritten text
- Multiple language support (140+ languages)
- Page layout information
- Text styles (handwritten vs. printed)
- Confidence scores

## Reference

- Azure Document Intelligence documentation: https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/
- Python SDK: https://learn.microsoft.com/en-us/python/api/overview/azure/ai-documentintelligence-readme

