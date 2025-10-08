# Google Cloud Vision API Setup

## Prerequisites

You need a Google Cloud Platform (GCP) account with Vision API enabled.

## Google Cloud Setup

1. **Create GCP Project:**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Create a new project or select an existing one

2. **Enable Vision API:**
   - In your project, go to "APIs & Services" > "Library"
   - Search for "Cloud Vision API"
   - Click "Enable"

3. **Create Service Account:**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "Service Account"
   - Fill in the details and click "Create"
   - Grant the "Cloud Vision API User" role
   - Click "Done"

4. **Create Service Account Key:**
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

Google Vision supports two authentication methods:

### Method 1: Environment Variable (Recommended)

Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable:

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-service-account-key.json"
```

Then use minimal config:
```yaml
ocr_systems:
  - name: "google_vision"
    type: "commercial_ocr"
    config:
      measure_time: true
```

### Method 2: Direct Credentials in Config

Extract fields from your service account JSON and add to config:

```yaml
ocr_systems:
  - name: "google_vision"
    type: "commercial_ocr"
    config:
      type: "service_account"
      project_id: "your-project-id"
      private_key_id: "your-private-key-id"
      private_key: "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
      client_email: "your-service-account@your-project.iam.gserviceaccount.com"
      client_id: "your-client-id"
      auth_uri: "https://accounts.google.com/o/oauth2/auth"
      token_uri: "https://oauth2.googleapis.com/token"
      auth_provider_x509_cert_url: "https://www.googleapis.com/oauth2/v1/certs"
      client_x509_cert_url: "https://www.googleapis.com/robot/v1/metadata/x509/..."
      universe_domain: "googleapis.com"
      measure_time: true
```

## API Limits and Pricing

- **Free tier**: 1,000 units per month
- **Rate limits**: 
  - TEXT_DETECTION: 1,800 images per minute
  - DOCUMENT_TEXT_DETECTION: 600 images per minute
- **Pricing**: Pay per 1,000 units after free tier
  - First 1,000 units/month: Free
  - 1,001 - 5,000,000 units/month: $1.50 per 1,000 units
  - 5,000,001+ units/month: $0.60 per 1,000 units

Refer to [Google Cloud Vision pricing](https://cloud.google.com/vision/pricing)

## Features

Google Cloud Vision API provides:
- High-quality text detection (TEXT_DETECTION)
- Document text detection (DOCUMENT_TEXT_DETECTION)
- Multi-language support (50+ languages)
- Handwriting detection
- Confidence scores
- Bounding boxes for detected text

## Supported Languages

Google Vision supports 50+ languages including:
- English, Spanish, French, German, Italian
- Chinese (Simplified & Traditional), Japanese, Korean
- Arabic, Hindi, Russian
- And many more

## Reference

- Google Cloud Vision documentation: https://cloud.google.com/vision/docs
- Python client library: https://cloud.google.com/python/docs/reference/vision/latest
- Pricing: https://cloud.google.com/vision/pricing

