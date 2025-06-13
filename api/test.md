# Amazon SageMaker Lambda Service

This service provides an AWS Lambda function that interacts with Amazon SageMaker endpoints to generate product summaries.

## Overview

The service uses a Llama 3 8B Instruct Model endpoint to:
- Generate individual product summaries
- Create comparative analyses of products within a category

## Technical Details

### Architecture
- AWS Lambda with Python Runtime
- Amazon SageMaker Endpoint Integration
- Serverless Framework for Deployment
- CORS-enabled HTTP endpoints

### Dependencies
- Python
- boto3
- pandas
- Serverless Framework

## API Endpoints

### POST /invoke
Generates product summaries or category analyses.

#### Request Body Format:
```json
{
    "category": "string",     // Optional: Category name for comparison analysis
    "id": "string",          // Optional: Product ID for single product analysis
    "summaries": []          // Optional: Array of product summaries
}
```

#### Response Format:
```json
{
    "statusCode": 200,
    "body": {
        "generated_text": "string"  // Generated text from LLM
    }
}
```

## Deployment

1. Install dependencies:
```bash
npm install
pip install -r requirements.txt
```

2. Deploy using Serverless Framework:
```bash
serverless deploy
```

## Environment Variables

- `ENDPOINT_NAME`: Name of the SageMaker endpoint (jumpstart-dft-llama-3-1-8b-instruct-20250613-043314)

## IAM Permissions

The service requires the following AWS permissions:
- SageMaker: InvokeEndpoint
- CloudWatch Logs: CreateLogGroup, CreateLogStream, PutLogEvents

## Data

The service uses a CSV file (`top3_products.csv`) for product information, containing:
- Product IDs (asins)
- Product names
- Categories (cluster_name)
- Positive and negative reviews
