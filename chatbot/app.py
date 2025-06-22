import json
import boto3
import time
from typing import Dict, Any

# Set this to True once you have Bedrock access enabled
USE_BEDROCK = False

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Text generation handler with Bedrock toggle"""
    
    try:
        # Debug: Print the entire event to CloudWatch logs
        print(f"Event received: {json.dumps(event)}")
        
        # Parse request - handle both direct invocation and API Gateway
        body_str = event.get('body')
        if body_str is None:
            body = event
        else:
            body = json.loads(body_str)
            
        prompt = body.get('prompt', body.get('message', ''))
        max_tokens = body.get('max_tokens', 1000)
        temperature = body.get('temperature', 0.7)
        user_id = body.get('user_id', 'anonymous')
        
        if not prompt:
            return {
                'statusCode': 400,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': 'Prompt is required'})
            }
        
        if USE_BEDROCK:
            # Real Bedrock call
            try:
                bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
                
                request_body = {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "messages": [{"role": "user", "content": prompt}]
                }
                
                response = bedrock.invoke_model(
                    modelId="anthropic.claude-sonnet-4-20250514-v1:0",
                    body=json.dumps(request_body)
                )
                
                response_body = json.loads(response['body'].read())
                generated_text = response_body['content'][0]['text']
                
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({
                        'generated_text': generated_text,
                        'metadata': {
                            'input_tokens': len(prompt.split()) * 1.3,
                            'output_tokens': len(generated_text.split()) * 1.3,
                            'response_time_ms': 200,
                            'model_id': 'anthropic.claude-sonnet-4-20250514-v1:0',
                            'user_id': user_id
                        }
                    })
                }
                
            except Exception as e:
                print(f"Bedrock error: {str(e)}")
                return {
                    'statusCode': 500,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error': f'Bedrock error: {str(e)}'})
                }
        else:
            # Mock response until Bedrock access is enabled
            mock_response = f"[MOCK] AI Generated Response for: '{prompt}'\n\nThis is a simulated Claude 4 Sonnet response. The actual AI response will be much more sophisticated once Bedrock model access is enabled.\n\nParameters used:\n- Max tokens: {max_tokens}\n- Temperature: {temperature}\n- User ID: {user_id}"
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'generated_text': mock_response,
                    'metadata': {
                        'input_tokens': len(prompt.split()),
                        'output_tokens': len(mock_response.split()),
                        'response_time_ms': 50,
                        'mock_mode': True,
                        'user_id': user_id,
                        'note': 'Enable Bedrock Claude 4 Sonnet access to get real AI responses'
                    }
                })
            }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'Internal server error: {str(e)}'})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'Internal server error: {str(e)}'})
        }

def get_usage_stats(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Simple usage stats for testing"""
    try:
        user_id = event['pathParameters'].get('user_id', 'anonymous')
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'user_id': user_id,
                'total_requests': 0,
                'total_tokens': 0,
                'test_mode': True
            })
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }