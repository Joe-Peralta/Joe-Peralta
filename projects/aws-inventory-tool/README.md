# AWS Inventory Tool

Small Python CLI for listing EC2 instances in an AWS account/region.

## What it does
- Uses `boto3` to call `DescribeInstances`
- Prints instance ID, state, type, and Name tag
- Reads AWS region/profile from environment variables
- Emits structured logs suitable for CLI troubleshooting

## Prerequisites
- Python 3.11+
- AWS credentials configured locally (profile or environment)

## Setup
```bash
cd projects/aws-inventory-tool
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copy `.env.example` values into your environment (do not commit secrets):
```bash
export AWS_PROFILE=default
export AWS_REGION=us-east-1
```

## Usage
```bash
python -m aws_inventory_tool.cli
```

Optional overrides:
```bash
python -m aws_inventory_tool.cli --profile my-profile --region us-west-2
```

## Tests
```bash
pytest tests -q
```
