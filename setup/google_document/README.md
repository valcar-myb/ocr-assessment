# Google Cloud Document AI Setup

## Prerequisites

You need a Google Cloud Platform (GCP) account with Document AI API enabled.

## Google Cloud Setup

1. **Create GCP Project:**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select an existing one

2. **Enable Document AI API:**
   - In your project, go to "APIs & Services" > "Library"
   - Search for "Cloud Document AI API"
   - Click "Enable"

3. **Create Document AI Processor:**
   - Go to "Document AI" in the console
   - Click "Create Processor"
   - Select "Document OCR" processor type
   - Choose a region (e.g., `us`, `eu`)
   - Note the Processor ID

4. **Create Service Account:**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Fill in the details and click "Create"
   - Grant the "Cloud Document AI API User" role
   - Click "Done"

5. **Create Service Account Key:**
   - Click on the created service account
   - Go to "Keys" tab
   - Click "Add Key" > "Create new key"
   - Select JSON format
   - Download the JSON key file

## Python Package Installation

```bash
pip install -r requirements.txt
```

## Configuration

Google Document AI supports two authentication methods:

### Method 1: Environment Variable (Recommended)

Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-service-account-key.json"
```

Then use minimal config:
```yaml
ocr_systems:
  - name: "google_document"
    type: "commercial_ocr"
    config:
      project_id: "your-project-id"
      location: "us"
      processor_id: "your-processor-id"
      field_mask: "text,pages.pageNumber,pages.blocks,pages.lines"
      measure_time: true
```

### Method 2: Direct Credentials in Config

Extract fields from your service account JSON and add to config (same as Google Vision).

## Configuration Parameters

- `project_id`: GCP project ID (required)
- `location`: Processor location (default: `us`) - Options: `us`, `eu`
- `processor_id`: Document AI processor ID (required)
- `processor_version_id`: Specific processor version (optional)
- `field_mask`: Fields to return in response (optional but recommended to reduce response size)
- Service account credentials (see Google Vision setup)
- `measure_time`: Measure processing time (default: `false`)

### Available Locations

- `us` (United States)
- `eu` (European Union)

## API Limits and Pricing

- **Free tier**: Not available for Document AI
- **Rate limits**: 
  - Online processing: 600 pages per minute
  - Batch processing: 10,000 pages per request
- **Pricing**: Pay per page processed
  - First 1,000 pages/month: $1.50 per 1,000 pages
  - 1,001-1,000,000 pages/month: $0.65 per 1,000 pages
  - 1,000,001+ pages/month: $0.30 per 1,000 pages

Refer to [Google Document AI pricing](https://cloud.google.com/document-ai/pricing)

## Features

Google Document AI OCR provides:
- High-quality text extraction
- Layout analysis
- Form parsing capabilities
- Support for 200+ languages
- Handwriting recognition
- Table extraction
- Advanced document understanding

## Processor Types

For OCR benchmarking, use:
- **Document OCR**: General-purpose OCR for any document type

Other available processors (for reference):
- Form Parser
- Invoice Parser
- Receipt Parser
- ID Document Parser
- Custom processors

## Reference

- Google Document AI documentation: https://cloud.google.com/document-ai/docs
- Python client library: https://cloud.google.com/python/docs/reference/documentai/latest
- Pricing: https://cloud.google.com/document-ai/pricing

