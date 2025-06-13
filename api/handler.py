"""
AWS Lambda handler to run inference
"""

import json
import boto3
import pandas as pd

# Initialize AWS SageMaker client for model inference
runtime_client = boto3.client('sagemaker-runtime')

# SageMaker endpoint configuration
ENDPOINT_NAME = "jumpstart-dft-llama-3-1-8b-instruct-20250613-043314"

# CORS headers for API responses
CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers':
    'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,X-Amz-User-Agent',
    'Access-Control-Allow-Methods': 'POST,OPTIONS'
}

def get_product_by_id(prod_id):
    """
    Retrieves a product from the CSV file based on its ID.
    
    Args:
        id (str): The product ID to search for
        
    Returns:
        pandas.Series: The product data if found, None otherwise
    """
    # Load and filter product data
    csv_data = pd.read_csv("./data/top3_products.csv")
    filtered_data = csv_data[csv_data['asins'].astype(str) == str(prod_id)]

    if filtered_data.empty:
        return None
    return filtered_data.iloc[0]

def safe_strip(value):
    """
    Safely strips whitespace from a string value.
    
    Args:
        value: The value to strip (can be any type)
        
    Returns:
        str: Stripped string
    """
    if isinstance(value, str):
        return value.strip()

    return ""

def get_top3_products_by_category(category):
    """
    Retrieves the top 3 products for a given category from the CSV file.
    
    Args:
        category (str): The category to filter products by
        
    Returns:
        pandas.DataFrame: DataFrame containing the filtered products
    """
    csv_data = pd.read_csv("./data/top3_products.csv")
    filtered_data = csv_data[csv_data['cluster_name'] == category]
    return filtered_data

def generate_final_summary_prompt(summaries):
    """
    Generates a prompt for creating a final summary of multiple product summaries.
    
    Args:
        category (str): The product category
        summaries (list): List of individual product summaries
        
    Returns:
        str: Formatted prompt for the language model
    """
    # Base prompt template for final summary
    prompt = """You are given three product summaries describing similar products.

Your task is to:

1. Write a final, article that combines the most important points from all three summaries.
2. Then write a clear paragraph stating which product is the best overall and why.

Please follow these instructions:

- Write in fluent, professional English.
- Focus on key features, advantages, and important drawbacks
- Return the output in valid markdown with headlines and paragraphs.\n\n.
"""

    # Add individual summaries to the prompt
    for i, sumary in enumerate(summaries):
        prompt += f"Summary {i + 1}:\n\n{sumary}\n\n"

    prompt += "---\n\nReturn ONLY the article. Do NOT check the grammar or add anything else."

    return prompt

def generate_product_summary_prompt(product):
    """
    Generates a prompt for summarizing a single product.
    
    Args:
        product (dict): Dictionary containing product information
        
    Returns:
        str: Formatted prompt for the language model
    """
    # Extract and clean product information
    name = product.get('name', 'Unnamed Product')
    positive = safe_strip(product.get('positive_reviews', ''))
    negative = safe_strip(product.get('negative_reviews', ''))

    prompt = (
        "Summarize the following product briefly and concisely. ",
        "Highlight its most important features, advantages, and possible disadvantages.\n\n"
        "---\n\n"
        f"{name}\n\n"
        f"Positive:{positive}\n\n"
        f"Negative:{negative}\n\n"
         "---\n\n"
        "Return the summary in one single paragraph in correct English."
    )

    return prompt

def call_model(prompt, max_new_tokens):
    """
    Calls the SageMaker endpoint with the given prompt.
    
    Args:
        prompt (str): The prompt to send to the language model
        
    Returns:
        dict: The model's response
    """

    # Call the model and parse response
    response = runtime_client.invoke_endpoint(
        EndpointName=ENDPOINT_NAME,
        ContentType='application/json',
        Body=json.dumps({"inputs": prompt, "parameters": { "max_new_tokens": max_new_tokens }})
    )
    result_str = response['Body'].read().decode('utf-8')
    return json.loads(result_str)

def lambda_handler(event, _):
    """
    AWS Lambda handler function that processes incoming requests.
    
    Args:
        event (dict): The event data from AWS Lambda
        context (object): The context object from AWS Lambda
        
    Returns:
        dict: Response containing status code, headers, and body
    """
    # Parse request body
    body = json.loads(event.get("body", "{}"))
    category = body.get("category", "")
    product_id = body.get("id", "")
    summaries = body.get("summaries", [])

    try:
        # Handle single product summary request
        if len(product_id) > 0:
            product = get_product_by_id(product_id)
            prompt = generate_product_summary_prompt(product)
            result = call_model(prompt, 400)
            return {
                "statusCode": 200,
                'headers': CORS_HEADERS,
                "body": json.dumps(result)
            }

        # Validate input for final summary
        if len(summaries) == 0 | len(category) == 0:
            return {
                "statusCode": 200,
                'headers': CORS_HEADERS,
                "body": json.dumps({"error": "Summaries and/or category are/is missing!"})
            }

        # Generate and return final summary
        prompt = generate_final_summary_prompt(summaries)
        result = call_model(prompt, 500)

        return {
            "statusCode": 200,
            'headers': CORS_HEADERS,
            "body": json.dumps(result)
        }

    except Exception as e:
        return {
            "statusCode": 500,
            'headers': CORS_HEADERS,
            "body": json.dumps({"error": f"Unexpected error: {str(e)}"})
        }
