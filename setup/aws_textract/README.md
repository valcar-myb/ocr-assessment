# AWS Textract Setup

## Prerequisites

You need an AWS account with Textract access enabled.

## AWS Credentials

Configure your AWS credentials using one of these methods:

### Method 1: AWS CLI Configuration
```bash
aws configure
```

### Method 2: Environment Variables
```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

### Method 3: Configuration File
Add credentials in `config/experiments.yaml` (see Configuration section below)

## Python Package Installation

```bash
pip install -r requirements.txt
```

## Configuration

AWS Textract supports the following parameters in `config/experiments.yaml`:

- `aws_access_key_id`: AWS access key ID (optional if using AWS CLI or env vars)
- `aws_secret_access_key`: AWS secret access key (optional if using AWS CLI or env vars)
- `region_name`: AWS region (default: `us-east-1`)
- `measure_time`: Measure processing time (default: `false`)

### Example Configuration

```yaml
ocr_systems:
  - name: "aws_textract"
    type: "commercial_ocr"
    config:
      region_name: "us-east-1"
      measure_time: true
      # Optional: Add credentials here if not using AWS CLI
      # aws_access_key_id: "your_access_key"
      # aws_secret_access_key: "your_secret_key"
```

## Supported AWS Regions

Common regions for Textract:
- `us-east-1` (US East - N. Virginia)
- `us-east-2` (US East - Ohio)
- `us-west-2` (US West - Oregon)
- `eu-west-1` (Europe - Ireland)
- `ap-southeast-2` (Asia Pacific - Sydney)

Check AWS documentation for full list of supported regions.

## API Limits and Pricing

- **Rate limits**: Check your AWS account limits
- **Pricing**: Pay per image processed
- Refer to AWS Textract pricing: https://aws.amazon.com/textract/pricing/

## Reference

AWS Textract documentation: https://docs.aws.amazon.com/textract/

